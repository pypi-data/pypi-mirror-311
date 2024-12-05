from typing import Any

from dbt.adapters.duckdb import DuckDBConnectionManager

from dbt.adapters.events.logging import AdapterLogger

logger = AdapterLogger("Fivetran")


class FivetranConnectionManager(DuckDBConnectionManager):
    TYPE = "fivetran"

    def execute_for_cursor(self, sql: str) -> Any:
        print(f" EXECUTE for cursor")
        sql = self._add_query_comment(sql)
        _, cursor = self.add_query(sql, True)
        response = self.get_response(cursor)
        print(f" ... resp: {response}")
        return cursor


