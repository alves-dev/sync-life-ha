from datetime import datetime

from peewee import (
    Model, Proxy, AutoField, CharField, IntegerField, DateTimeField,
    SqliteDatabase, BooleanField, DoubleField
)

from .model_enum import GroupingType, EnumField, RecordType, Periodicity, ValueTrend, Grouping, PaymentMethod, \
    GroupingPerson

db_proxy = Proxy()

TABLE_PREFIX = 'finance'


def init_finance_db(db: SqliteDatabase) -> None:
    db_proxy.initialize(db)
    db.create_tables([FinancePlan, PlanTransaction])


class BaseModel(Model):
    class Meta:
        database = db_proxy


class FinancePlan(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()
    type = EnumField(RecordType)
    periodicity = EnumField(Periodicity)
    active = BooleanField()
    day_movement = IntegerField(null=True)
    month_movement = IntegerField(null=True)
    value = DoubleField(null=True)
    value_exact = BooleanField()
    value_trend = EnumField(ValueTrend, null=True)
    essential = BooleanField()
    grouping = EnumField(Grouping, null=True)
    grouping_person = EnumField(GroupingPerson, null=True)
    grouping_type = EnumField(GroupingType, null=True)
    payment_method = EnumField(PaymentMethod, null=True)
    created_on = DateTimeField(default=datetime.now)
    updated_in = DateTimeField(default=datetime.now)

    class Meta:
        table_name = f'{TABLE_PREFIX}_plan'


class PlanTransaction(BaseModel):
    id = AutoField(primary_key=True)
    id_finance_plan = IntegerField()
    month = IntegerField()
    created_on = DateTimeField(default=datetime.now)
    person_id = CharField()

    class Meta:
        table_name = f'{TABLE_PREFIX}_plan_transaction'

    def key(self) -> str:
        return f'{self.id_finance_plan}-{self.month}'
