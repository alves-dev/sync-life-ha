from enum import Enum


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
