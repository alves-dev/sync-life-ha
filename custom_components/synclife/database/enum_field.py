from peewee import Field


class EnumField(Field):
    field_type = 'VARCHAR'

    def __init__(self, enum_class, *args, **kwargs):
        self.enum_class = enum_class
        super().__init__(*args, **kwargs)

    def db_value(self, value):
        if isinstance(value, self.enum_class):
            return value.name
        elif value is None:
            return None
        else:
            raise TypeError(f"Valor inválido para EnumField: {value}")

    def python_value(self, value):
        if value is not None:
            return self.enum_class[value]
        return None
