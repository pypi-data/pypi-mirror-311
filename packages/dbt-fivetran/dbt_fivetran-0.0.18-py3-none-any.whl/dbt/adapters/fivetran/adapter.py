
import boto3
import os
import pyarrow as pa

from dbt.adapters.duckdb import DuckDBAdapter
from dbt.adapters.fivetran.connections import FivetranConnectionManager
from dbt.adapters.base import BaseRelation
from dbt.adapters.base.meta import available
from multiprocessing.context import SpawnContext

from io import UnsupportedOperation
from typing import Optional, List
from pyiceberg.catalog import load_catalog

import logging

logger = logging.getLogger(__name__)

# DuckDB to Iceberg type mappings
TYPE_MAPPINGS = {
    'bool': pa.bool_(),
    'boolean': pa.bool_(),
    'tinyint': pa.int8(),
    'smallint': pa.int16(),
    'integer': pa.int32(),
    'bigint': pa.int64(),
    'number': pa.int64(),  # Assuming 'number' corresponds to int64
    'utinyint': pa.uint8(),
    'usmallint': pa.uint16(),
    'uinteger': pa.uint32(),
    'ubigint': pa.uint64(),
    'float': pa.float32(),
    'double': pa.float64(),
    'varchar': pa.string(),
    'string': pa.string(),
    'text': pa.string(),
    'char': pa.string(),
    'date': pa.date32(),
    'time': pa.time64('us'),
    'datetime': pa.timestamp('us'),
    'timestamp': pa.timestamp('us'),
    'json': pa.string(),
    'timestamp with time zone': pa.timestamp('us', tz='UTC'),
    'blob': pa.binary(),
    'hugeint': pa.decimal128(38, 0),  # Assuming 38 digits precision for hugeint
    'uuid': pa.string()  # PyArrow doesn't have a native UUID type
}

DEFAULT_BATCH_SIZE = 250_000

def dbg_print(msg: str):
    pass
    #print(msg)

class FivetranAdapter(DuckDBAdapter):
    adapter_type = "fivetran"

    Relation = BaseRelation
    ConnectionManager = FivetranConnectionManager
    connections: FivetranConnectionManager

    def __init__(self, config, mp_context: SpawnContext) -> None:
        secrets = config.credentials.get_secrets()
        if secrets.type.lower() == 's3':
            boto3.setup_default_session(
                aws_access_key_id=secrets.secret_kwargs['key_id'],
                aws_secret_access_key=secrets.secret_kwargs['secret'],
                region_name=secrets.secret_kwargs['region'],
            )
            self.storage_client = boto3.client('s3')
        else:
            raise ValueError("Only S3 is supported at the moment")

        self.database = config.credentials.database
        if getattr(config, 'clean_targets', None):
            if 'target' in config.clean_targets:
                db_folder = os.path.join(os.getcwd(), 'target')
            else:
                db_folder = os.getcwd()
        else:
            db_folder = None

        if db_folder:
            config.credentials.path = os.path.join(db_folder, f"{self.database}.local.db")

        self.catalog = load_catalog("polaris_rest",
            **{
                "uri": f"{config.credentials.polaris_uri}/api/catalog",
                "credential": config.credentials.polaris_credentials,
                "scope": config.credentials.polaris_scope,
                "warehouse": config.credentials.polaris_catalog
            }
        )
        super().__init__(config, mp_context)

    def create_schema(self, relation: BaseRelation) -> None:
        dbg_print(f"CREATE SCHEMA: {relation} | {relation.schema}")

        self.catalog.create_namespace_if_not_exists(relation.schema)
        super().create_schema(relation)

    def _get_local_views(self, schema_relation: BaseRelation) -> List[BaseRelation]:
        kwargs = {"schema_relation": schema_relation}
        results = self.execute_macro("list_relations_without_caching", kwargs=kwargs)
        relations = []
        quote_policy = {"database": True, "schema": True, "identifier": True}
        for _database, name, _schema, _type in results:
            try:
                _type = self.Relation.get_relation_type(_type)
            except ValueError:
                _type = self.Relation.External
            relations.append(
                BaseRelation.create(
                    database=_database,
                    schema=_schema,
                    identifier=name,
                    quote_policy=quote_policy,
                    type=_type,
                )
            )
        return relations

    def list_relations_without_caching(self, relation: BaseRelation) -> List[BaseRelation]:
        dbg_print(f"LIST RELATIONS: {relation.database} {relation.schema} {relation.identifier}")

        # Get views from local db if any
        relations = self._get_local_views(relation)

        # Get tables from polaris catalog
        try:
            for table in self.catalog.list_tables(relation.schema):
                relations.append(
                    BaseRelation.create(
                        database=self.database, schema=table[0], identifier=table[1]))
        except:
            pass

        dbg_print(f"  RELATIONS: {relations}")
        return relations

    @staticmethod
    def _relation_to_identifier(relation: BaseRelation) -> str:
        return f"{relation.schema}.{relation.identifier}"

    def _check_location(self, relation):
        response = self.storage_client.list_objects_v2(
            Bucket=relation.database,
            Prefix=f"{relation.schema}/{relation.identifier}/",
            MaxKeys=1)
        return 'Contents' in response

    @available
    def create_table_as(self, temporary: bool, relation: BaseRelation, sql: str):
        dbg_print(f"CREATE TABLE AS: {temporary} {relation.schema} {relation.identifier}")

        if temporary:
            raise UnsupportedOperation("Temporary tables are not supported")

        connection = self.acquire_connection()
        self.connections.open(connection)

        cursor = self.connections.execute_for_cursor(f"describe select * from ({sql})")
        column_names = []
        schema_cols = []
        for desc in cursor.fetchall():
            col_name = desc[0]
            col_type = desc[1]
            column_names.append(col_name)
            schema_cols.append((col_name, TYPE_MAPPINGS[col_type.lower()]))
        schema = pa.schema(schema_cols)

        table_identifier = self._relation_to_identifier(relation)
        location_exists = self._check_location(relation)
        location_identifier = f"{relation.identifier}_2" if location_exists else relation.identifier
        location = f"s3://{relation.database}/{relation.schema}/{location_identifier}"
        table = self.catalog.create_table(
            identifier=table_identifier,
            schema=schema,
            location=location,
            properties={
                "write.parquet.compression-codec": "snappy"
            }
        )
        dbg_print(f"  .... table created: {table_identifier} @ {location}")

        cursor = self.connections.execute_for_cursor(sql)
        batch_reader = cursor.fetch_record_batch(rows_per_batch=DEFAULT_BATCH_SIZE)
        while True:
            try:
                batch = batch_reader.read_next_batch()
            except StopIteration:
                break

            pa_table = pa.Table.from_batches([batch], schema=schema)
            table.append(pa_table)

        table.refresh()
        dbg_print(f"  .... data appended to table")

        # Create a view for the table so it is easy to query from duckdb
        self._create_db_view_from_iceberg(relation.schema, relation.table, table.metadata_location)

    def _get_table_location(self, schema: str, table: str):
        dbg_print(f"GET LOCATION {schema} {table}")
        ent = f"{schema}.{table}"
        if self.catalog.table_exists(ent):
            table = self.catalog.load_table(ent)
            return table.metadata_location
        return None

    def _create_db_schema(self, schema):
        try:
            self.connections.execute(f"CREATE SCHEMA {schema}")
            dbg_print(f" created db schema: {schema}")
        except Exception as e:
            if "already exists" not in str(e):
                raise e

    def _create_db_view_from_iceberg(self, schema: str, table: str, location_metadata: str):
        self._drop_db_view_if_exists(schema, table)
        sql = f'CREATE VIEW "{self.database}"."{schema}"."{table}" AS (SELECT * FROM iceberg_scan("{location_metadata}"))'
        self.connections.execute(sql)
        dbg_print(f" created db view: {schema} {table} {location_metadata}")

    def _drop_db_view_if_exists(self, schema: str, table: str) -> str:
        identifier = f"{schema}.{table}"
        try:
            self.connections.execute(f"DROP VIEW {identifier}")
            dbg_print(f" dropped db schema: {schema}")
        except Exception as e:
            if f"View with name {table} does not exist" not in str(e):
                raise e
        return identifier

    @available
    def handle_source(self, schema, table, fetcher=_get_table_location) -> Optional[BaseRelation]:
        location = fetcher(self,schema, table)
        dbg_print(f"HANDLE SOURCE: {schema} {table} {location}")

        if location:
            # we need to wrap iceberg tables in views so we can use them in complex queries
            connection = self.acquire_connection()
            self.connections.open(connection)
            self._create_db_schema(schema)
            identifier = self._drop_db_view_if_exists(schema, table)
            sql = f"CREATE VIEW {identifier} AS SELECT * FROM iceberg_scan(\"{location}\")"
            self.connections.execute(sql)

        return BaseRelation.create(database=self.database, schema=schema, identifier=table)

    def drop_relation(self, relation):
        dbg_print(f" DROP RELATION: {relation} | {relation.type}")

        if relation.type == "view":
            super().drop_relation(relation)
        else:
            self._drop_table(relation)

    def _drop_table(self, relation: BaseRelation):
        dbg_print(f" DROP TABLE: {relation}")

        identifier = self._relation_to_identifier(relation)
        try:
            table = self.catalog.load_table(identifier)
            metadata_location = table.metadata_location
        except:
            metadata_location = None

        dbg_print(f" --- metadata loc: {metadata_location}")

        if self.catalog.table_exists(identifier):
            self.catalog.drop_table(identifier)

        if metadata_location:
            self._delete_iceberg_table(relation, metadata_location)

    def _delete_iceberg_table(self, relation: BaseRelation, metadata_location: str):
        dbg_print(f" DEL ICE TABLE: {metadata_location}")

        bucket = relation.database
        identifiers = metadata_location.split('/')
        identifier = identifiers[-3]
        prefix = f"{relation.schema}/{identifier}"
        objects_to_delete = self.storage_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        if 'Contents' in objects_to_delete:
            delete_keys = [{'Key': obj['Key']} for obj in objects_to_delete['Contents'] if f"{identifier}/" in obj['Key']]
            self.storage_client.delete_objects(Bucket=bucket, Delete={'Objects': delete_keys})
            dbg_print(f"Deleted {len(delete_keys)} objects")

    def rename_relation(self, from_relation: BaseRelation, to_relation: BaseRelation):
        dbg_print(f">> RENAME_RELATION: {from_relation} {from_relation.type} {to_relation}")
        dbg_print(f"    -- {from_relation.schema}.{from_relation.identifier} -> {to_relation.schema}.{to_relation.identifier}")

        if from_relation.type == "view":
            dbg_print(f"      .... rename view")
            super().rename_relation(from_relation, to_relation)
        else:
            dbg_print(f"      .... rename table")
            from_table = self._relation_to_identifier(from_relation)
            if self.catalog.table_exists(from_table):
                to_table = self._relation_to_identifier(to_relation)
                if self.catalog.table_exists(to_table):
                    raise ValueError(f"TO TABLE {to_table} exists")
                self.catalog.rename_table(from_table, to_table)