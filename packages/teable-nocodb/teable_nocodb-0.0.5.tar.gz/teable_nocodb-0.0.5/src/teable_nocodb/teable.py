from typing import Any
import requests
from .data_type import FieldType


class Teable:
    def __init__(self, base_url: str, api_key: str):
        self.api_url = base_url + "/api"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json",
        }

    def __str__(self) -> str:
        return f"Teable API at {self.api_url}"

    def __repr__(self) -> str:
        return f"Teable(base_url='{self.api_url}', api_key='***')"

    def get_tables(self, base_id: str) -> list["Table"]:
        response = requests.get(
            f"{self.api_url}/base/{base_id}/table",
            headers=self.headers,
        )
        if response.status_code == 200:
            tables = [Table(**t, teable=self) for t in response.json()]
            return tables
        else:
            raise Exception(
                f"Failed to fetch tables with status code: {response.status_code}, message: {response.text}"
            )

    def create_table(self, base_id: str, table_data: "Table") -> "Table":
        response = requests.post(
            f"{self.api_url}/base/{base_id}/table",
            json=table_data.to_dict(),
            headers=self.headers,
        )
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(
                f"Failed to create table with status code: {response.status_code}, message: {response.text}"
            )


class Table:
    def __init__(
        self,
        name: str,
        dbTableName: str,
        fields: list["Field"] | None = None,
        teable: Teable | None = None,
        id: str | None = None,
        **kwargs: str,
    ) -> None:
        self.teable = teable
        self.name = name
        self.dbTableName = dbTableName
        self.fields = fields or []
        self.table_id = id
        self.meta = kwargs
        self.records: list[list[dict[str, str]]] = []

    def __str__(self) -> str:
        return f"Table '{self.name}' (DB Table: {self.dbTableName})"

    def __repr__(self) -> str:
        return f"Table(name='{self.name}', dbTableName='{self.dbTableName}', fields={self.fields})"

    def get_fields(self) -> list["Field"]:
        if self.teable is None:
            raise Exception("Teable instance is not provided.")

        response = requests.get(
            f"{self.teable.api_url}/table/{self.table_id}/field",
            headers=self.teable.headers,
        )
        if response.status_code == 200:
            self.fields = [
                Field(teable=self.teable, field_type=f["type"], **f)
                for f in response.json()
            ]
            return self.fields
        else:
            raise Exception(
                f"Failed to fetch table fields with status code: {response.status_code}, message: {response.text}"
            )

    def to_dict(
        self,
    ) -> dict[
        str,
        str
        | list[dict[str, str | dict[str, list[dict[str, str]]]]]
        | list[list[dict[str, str]]],
    ]:
        return {
            "name": self.name,
            "dbTableName": self.dbTableName,
            "fields": [field.to_dict() for field in self.fields],
            "records": self.records,
        }


class SingleSelectOptions:
    def __init__(self, choices: list[dict[str, str]], **kwargs: str) -> None:
        self.choices = choices
        self.meta = kwargs

    def __str__(self) -> str:
        return f"SingleSelectOptions ({len(self.choices)} choices)"

    def __repr__(self) -> str:
        return f"SingleSelectOptions(choices={self.choices})"

    def to_dict(self) -> dict[str, list[dict[str, str]]]:
        return {"choices": self.choices}


class DateOptions:
    def __init__(
        self, date: str, time: str = "None", timezone: str = "utc", **kwargs: str
    ) -> None:
        self.date = date
        self.time = time
        self.timezone = timezone
        self.meta = kwargs

    def __str__(self) -> str:
        return f"DateOptions ({self.date}, {self.time}, {self.timezone})"

    def __repr__(self) -> str:
        return f"DateOptions(date='{self.date}', time='{self.time}', timezone='{self.timezone}')"

    def to_dict(self) -> dict[str, dict[str, str]]:
        return {
            "formatting": {
                "date": self.date,
                "time": self.time,
                "timeZone": self.timezone,
            }
        }


class RatingOptions:
    def __init__(self, color: str, icon: str, max: int) -> None:
        self.color = color
        self.icon = icon
        self.max = max

    def __str__(self) -> str:
        return f"RatingOptions ({self.color}, {self.icon}, {self.max})"

    def __repr__(self) -> str:
        return (
            f"RatingOptions(color='{self.color}', icon='{self.icon}', max='{self.max}')"
        )

    def to_dict(self) -> dict[str, str | int]:
        return {"color": self.color, "icon": self.icon, "max": self.max}


class Field:
    def __init__(
        self,
        name: str,
        dbFieldName: str,
        field_type: str | FieldType,
        options: dict[str, Any] | SingleSelectOptions | DateOptions | RatingOptions,
        notNull: bool | None = None,
        teable: Teable | None = None,
        **kwargs: str,
    ) -> None:
        self.teable = teable
        self.name = name
        self.dbFieldName = dbFieldName
        if isinstance(field_type, FieldType):
            self.field_type = field_type
        else:
            self.field_type = FieldType.from_teable(field_type)
        self.notNull = notNull
        self.options = options
        if isinstance(options, dict):
            if self.field_type == FieldType.SINGLE_SELECT:
                self.options = SingleSelectOptions(options["choices"])
            elif self.field_type == FieldType.DATE:
                self.options = DateOptions(**options["formatting"], **options)
            elif self.field_type == FieldType.RATING:
                self.options = RatingOptions(**options)
        self.meta = kwargs

    def __str__(self) -> str:
        return f"Field '{self.name}' (DB Field: {self.dbFieldName})"

    def __repr__(self) -> str:
        return f"Field(name='{self.name}', dbFieldName='{self.dbFieldName}', field_type={self.field_type}, options={self.options})"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "dbFieldName": self.dbFieldName,
            "type": self.field_type.teable_value,
            "options": self.options.to_dict()
            if isinstance(self.options, SingleSelectOptions)
            or isinstance(self.options, DateOptions)
            else self.options,
        }
