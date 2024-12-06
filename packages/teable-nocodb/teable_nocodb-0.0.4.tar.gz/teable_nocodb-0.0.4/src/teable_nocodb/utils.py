from math import e
from typing import Any
from .nocodb import Table as NocoTable, Column as NocoField
from .teable import (
    Table as TeaTable,
    Field as TeaField,
    SingleSelectOptions as TeaSSOption,
    DateOptions as TeaDateOption,
)
from .data_type import FieldType as ft


def fieldToTeable(field: NocoField) -> TeaField:
    if field.data_type == ft.SINGLE_SELECT:
        options = TeaSSOption(choices=[{"name": o.title} for o in field.options])
    elif field.data_type == ft.DATE:
        options = TeaDateOption(
            date="MM/DD/YYYY",
        )

    return TeaField(
        name=field.title,
        dbFieldName=field.column_name,
        field_type=field.data_type,
        notNull=field.required,
        options=options if field.data_type in [ft.SINGLE_SELECT, ft.DATE] else {},
    )


banned_field_type = [
    ft.ID,
    ft.ATTACHMENT,
    ft.MULTIPLE_SELECT,
    ft.FORMULA,
    ft.ROLLUP,
    ft.COUNT,
    ft.LINK,
    ft.BUTTON,
    ft.LINKS,
    ft.AUTO_NUMBER,
    ft.CREATED_TIME,
    ft.CREATED_BY,
    ft.LAST_MODIFIED_BY,
    ft.LAST_MODIFIED_TIME,
    ft.FOREIGN_KEY,
]


def tableToTeable(table: NocoTable) -> TeaTable:
    if table.columns is None:
        raise Exception("Table columns are not fetched.")
    fields: list[TeaField] = []
    for f in table.columns:
        if f.data_type not in banned_field_type:
            fields.append(fieldToTeable(f))
    return TeaTable(
        name=table.title,
        dbTableName=table.table_name,
        fields=fields,
    )
