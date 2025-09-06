from datetime import datetime

from peewee import (
    Model, Proxy, AutoField, CharField, IntegerField, DateTimeField,
    ForeignKeyField, SqliteDatabase, FloatField, BooleanField
)

db_proxy = Proxy()

TABLE_PREFIX = 'vehicle'


def init_vehicle_db(db: SqliteDatabase) -> None:
    db_proxy.initialize(db)
    db.create_tables([Vehicle, VehicleMileage, VehicleMaintenance])


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


class VehicleMaintenance(BaseModel):
    id = AutoField()
    vehicle = ForeignKeyField(Vehicle, backref="maintenances", on_delete="CASCADE")
    type = CharField()  # "oil_change", "revision", "alignment", "insurance", ...
    last_date = DateTimeField(null=True)
    last_mileage = IntegerField(null=True)
    next_date = DateTimeField(null=True)
    next_mileage = IntegerField(null=True)
    percentage = FloatField(null=True)
    bool_required = BooleanField(default=False)  # True se precisa fazer algo agora
    note = CharField(null=True)

    class Meta:
        table_name = f'{TABLE_PREFIX}_maintenance'
