from datetime import datetime

from peewee import (
    Model, Proxy, AutoField, CharField, IntegerField, DateTimeField,
    ForeignKeyField, SqliteDatabase
)

db_proxy = Proxy()

TABLE_PREFIX = 'vehicle'


def init_vehicle_db(db: SqliteDatabase) -> None:
    db_proxy.initialize(db)
    db.create_tables([Vehicle, VehicleMileage])


class BaseModel(Model):
    class Meta:
        database = db_proxy


class Vehicle(BaseModel):
    id = AutoField()
    name = CharField()
    brand = CharField()
    plate = CharField()
    model = CharField()
    year = IntegerField()

    class Meta:
        table_name = f'{TABLE_PREFIX}_main'


class VehicleMileage(BaseModel):
    id = AutoField()
    vehicle = ForeignKeyField(Vehicle, backref="mileages", on_delete="CASCADE")
    mileage = IntegerField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        table_name = f'{TABLE_PREFIX}_mileage'
