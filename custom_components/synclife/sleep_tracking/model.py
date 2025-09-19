from datetime import datetime

from peewee import (
    Model, Proxy, AutoField, CharField, IntegerField, DateTimeField,
    SqliteDatabase, BooleanField
)

from .model_enum import Action
from ..database.enum_field import EnumField

db_proxy = Proxy()

TABLE_PREFIX = 'sleep'


def init_sleep_db(db: SqliteDatabase) -> None:
    db_proxy.initialize(db)
    db.create_tables([SleepTracking])


class BaseModel(Model):
    class Meta:
        database = db_proxy


class SleepTracking(BaseModel):
    id = AutoField()
    person = CharField()
    created_at = DateTimeField(default=datetime.now)
    action = EnumField(Action)
    computed = BooleanField(default=False)
    minutes_slept = IntegerField(default=0)

    class Meta:
        table_name = f'{TABLE_PREFIX}_tracking'
