from datetime import datetime

from peewee import (
    Model, Proxy, AutoField, CharField, DateTimeField,
    SqliteDatabase, IntegerField
)

db_proxy = Proxy()

TABLE_PREFIX = 'nutrition'


def init_nutrition_db(db: SqliteDatabase) -> None:
    db_proxy.initialize(db)
    db.create_tables([SupplementIntake])


class BaseModel(Model):
    class Meta:
        database = db_proxy


class SupplementIntake(BaseModel):
    """Registro de ingestão de suplemento."""
    id = AutoField()
    person = CharField(null=False)
    supplement = CharField(null=False)
    taken_at = DateTimeField(default=datetime.now)
    amount = IntegerField(null=False)

    class Meta:
        table_name = f"{TABLE_PREFIX}_supplement_intake"
