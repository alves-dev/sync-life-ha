from datetime import datetime

from peewee import (
    Model, Proxy, AutoField, CharField, DateTimeField,
    ForeignKeyField, SqliteDatabase, IntegerField
)

db_proxy = Proxy()

TABLE_PREFIX = 'nutrition'


def init_nutrition_db(db: SqliteDatabase) -> None:
    db_proxy.initialize(db)
    db.create_tables([Supplement, SupplementIntake])


class BaseModel(Model):
    class Meta:
        database = db_proxy


class Supplement(BaseModel):
    """Cadastro de suplementos disponíveis."""
    id = AutoField()
    name = CharField(unique=True)
    dose_grams = IntegerField(null=False)

    class Meta:
        table_name = f"{TABLE_PREFIX}_supplement"


class SupplementIntake(BaseModel):
    """Registro de ingestão de suplemento."""
    id = AutoField()
    person = CharField()
    supplement = ForeignKeyField(Supplement, backref="intakes", on_delete="CASCADE")
    taken_at = DateTimeField(default=datetime.now)
    amount_grams = IntegerField(null=False)

    class Meta:
        table_name = f"{TABLE_PREFIX}_supplement_intake"
