import requests
from .data_type import FieldType


class NocoDB:
    def __init__(self, base_url: str, api_key: str):
        self.api_url = base_url + "/api/v2/meta"
        self.headers = {"xc-token": api_key, "Content-Type": "application/json"}

    def __str__(self) -> str:
        return f"NocoDB API at {self.api_url}"

    def __repr__(self) -> str:
        return f"NocoDB(base_url='{self.api_url}', api_key='***')"

    def get_tables(self, base_id: str) -> list["Table"]:
        response = requests.get(
            f"{self.api_url}/bases/{base_id}/tables", headers=self.headers
        )
        if response.status_code == 200:
            tables = [Table(self, **t) for t in response.json()["list"]]
            return tables
        else:
            raise Exception(
                f"Failed to fetch tables with status code: {response.status_code}"
            )


class Table:
    def __init__(
        self,
        nocodb: NocoDB | None = None,
        columns: list["Column"] | None = None,
        **kwargs: str,
    ) -> None:
        self.nocodb = nocodb
        self.base_id: str = kwargs["base_id"]
        self.table_id: str = kwargs["id"]
        self.title: str = kwargs["title"]
        self.table_name: str = kwargs["table_name"]
        self.columns = columns
        self.meta = kwargs

    def __str__(self) -> str:
        return f"Table '{self.title}' (ID: {self.table_id}, Base: {self.base_id})"

    def __repr__(self) -> str:
        return f"Table(base_id='{self.base_id}', table_id='{self.table_id}', title='{self.title}', columns={self.columns})"

    def get_columns(self) -> list["Column"]:
        if self.nocodb is None:
            raise Exception("NocoDB instance is not provided.")
        response = requests.get(
            f"{self.nocodb.api_url}/tables/{self.table_id}", headers=self.nocodb.headers
        )
        if response.status_code == 200:
            self.columns = [
                Column(nocodb=self.nocodb, **c) for c in response.json()["columns"]
            ]
            return self.columns
        else:
            raise Exception(
                f"Failed to fetch table columns with status code: {response.status_code}"
            )


class Column:
    def __init__(
        self,
        colOptions: dict[str, list[dict[str, str]]] | None = None,
        nocodb: NocoDB | None = None,
        **kwargs: str,
    ) -> None:
        self.nocodb = nocodb
        self.title: str = kwargs["title"]
        self.column_name: str = kwargs["column_name"]
        self.column_id: str = kwargs["id"]
        self.table_id: str = kwargs["fk_model_id"]
        self.system = bool(kwargs["system"])
        self.primary_key = bool(kwargs["pk"])
        if isinstance(kwargs["uidt"], FieldType):
            self.data_type = FieldType(kwargs["uidt"])
        else:
            self.data_type = FieldType.from_nocodb(kwargs["uidt"])
        self.meta = kwargs
        self.required = bool(kwargs["rqd"])
        self.options = []
        if self.data_type == FieldType.SINGLE_SELECT and colOptions is not None:
            self.options = [Option(**o) for o in colOptions["options"]]

    def __str__(self) -> str:
        return f"Column '{self.title}' (ID: {self.column_id}, Table: {self.table_id})"

    def __repr__(self) -> str:
        return f"Column(title='{self.title}', column_name='{self.column_name}', column_id='{self.column_id}', table_id='{self.table_id}', system={self.system}, primary_key={self.primary_key}, data_type='{self.data_type}')"


class Option:
    def __init__(self, title: str, color: str = "") -> None:
        self.title = title
        self.color = color

    def __str__(self) -> str:
        return f"Options '{self.title}'"

    def __repr__(self) -> str:
        return f"Options(name='{self.title}')"
