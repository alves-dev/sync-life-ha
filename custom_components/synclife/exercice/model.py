from datetime import datetime

from peewee import (
    Model, Proxy, AutoField, CharField, IntegerField, DateTimeField,
    SqliteDatabase, BooleanField
)

from .model_enum import Action
from ..database.enum_field import EnumField

db_proxy = Proxy()

TABLE_PREFIX = 'exercise'


def init_exercise_db(db: SqliteDatabase) -> None:
    db_proxy.initialize(db)
    db.create_tables([ExerciseAcademy])


class BaseModel(Model):
    class Meta:
        database = db_proxy


class ExerciseAcademy(BaseModel):
    id = AutoField()
    person = CharField()
    created_at = DateTimeField(default=datetime.now)
    action = EnumField(Action)
    computed = BooleanField(default=False)
    minutes_stay = IntegerField(default=0)

    class Meta:
        table_name = f'{TABLE_PREFIX}_academy'
