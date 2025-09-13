from enum import Enum

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


class RecordType(Enum):
    DESPESA = "DESPESA"
    RECEITA = "RECEITA"


class Periodicity(Enum):
    MENSAL = 'MENSAL'
    ANUAL = 'ANUAL'


class ValueTrend(Enum):
    AUMENTAR = 'AUMENTAR'
    MANTER = 'MANTER'
    DIMINUIR = 'DIMINUIR'


class Grouping(Enum):
    APARTAMENTO_US = "APARTAMENTO US"
    APARTAMENTO_ARAUCARIAS = "RECEITA"
    APARTAMENTO_ROOSEVELT = 'APARTAMENTO ROOSEVELT'
    CASA_SHOPPING_PARK = 'CASA SHOPPING PARK'
    SAUDE = 'SAÚDE'
    TRABALHO = 'TRABALHO'
    TERRENO = 'TERRENO'
    CARRO = 'CARRO'
    EDUCACAO = 'EDUCAÇÃO'
    LAZER = 'LAZER'
    COMUNICACAO = 'COMUNICAÇÃO'


class GroupingPerson(Enum):
    TODOS = "TODOS"
    JADE = "JADE"
    IGOR = 'IGOR'
    DAIARA = 'DAIARA'


class GroupingType(Enum):
    INTERNET = "INTERNET"
    ALUGUEL = "ALUGUEL"
    IMPOSTO = 'IMPOSTO'


class PaymentMethod(Enum):
    PIX = "PIX"
    BOLETO = "BOLETO"
    CARTAO = 'CARTÃO'
    DEBITO_CREDITO_CONTA = 'DEBITO_CREDITO_CONTA'
