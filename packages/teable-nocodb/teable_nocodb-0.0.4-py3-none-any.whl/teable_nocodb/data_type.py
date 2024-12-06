from enum import Enum


class FieldType(Enum):
    """Enumeration of field types in NocoDB and Teable."""

    ID = ("ID", "singleLineText")
    SINGLE_LINE_TEXT = ("SingleLineText", "singleLineText")
    LONG_TEXT = ("LongText", "longText")
    USER = ("User", "user")
    ATTACHMENT = ("Attachment", "attachment")
    CHECKBOX = ("Checkbox", "checkbox")
    MULTIPLE_SELECT = ("MultiSelect", "multipleSelect")
    SINGLE_SELECT = ("SingleSelect", "singleSelect")
    DATE = ("Date", "date")
    TIME = ("Time", "singleLineText")
    NUMBER = ("Number", "number")
    DECIMAL = ("Decimal", "number")
    CURRENCY = ("Currency", "number")
    DURATION = ("Duration", "number")
    RATING = ("Rating", "rating")
    FORMULA = ("Formula", "formula")
    ROLLUP = ("Rollup", "rollup")
    COUNT = ("Count", "count")
    CREATED_TIME = ("CreatedTime", "createdTime")
    LAST_MODIFIED_TIME = ("LastModifiedTime", "lastModifiedTime")
    CREATED_BY = ("CreatedBy", "createdBy")
    LAST_MODIFIED_BY = ("LastModifiedBy", "lastModifiedBy")
    AUTO_NUMBER = ("AutoNumber", "autoNumber")
    BUTTON = ("Button", "button")
    PHONE_NUMBER = ("PhoneNumber", "singleLineText")
    EMAIL = ("Email", "singleLineText")
    URL = ("URL", "singleLineText")
    LINK = ("LinkToAnotherRecord", "link")  # N-1 or 1-1 relationship
    LINKS = ("Links", "singleLineText")  # 1-N relationship
    FOREIGN_KEY = ("ForeignKey", "singleLineText")  # _id of another table

    def __init__(self, nocodb_value: str, teable_value: str):
        self.nocodb_value = nocodb_value
        self.teable_value = teable_value

    @classmethod
    def from_nocodb(cls, field_type: str):
        """Convert from NocoDB field type to FieldType."""
        for f in cls:
            if f.nocodb_value == field_type:
                return f
        raise ValueError(f"No matching FieldType for NocoDB value: {field_type}")

    @classmethod
    def from_teable(cls, field_type: str):
        """Convert from Teable field type to FieldType."""
        for f in cls:
            if f.teable_value == field_type:
                return f
        raise ValueError(f"No matching FieldType for Teable value: {field_type}")

    def to_nocodb(self):
        """Get the NocoDB representation of this field type."""
        return self.nocodb_value

    def to_teable(self):
        """Get the Teable representation of this field type."""
        return self.teable_value
