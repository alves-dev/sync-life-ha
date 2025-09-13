from datetime import datetime
from typing import cast

from .model import FinancePlan, PlanTransaction
from .model_enum import RecordType, Periodicity, PaymentMethod


def get_values_for_sensors_total_monthly() -> dict:
    """
    Retorna valores mensais:
        - Total receita
        - Total despesa
        - diferença = receita - despesa
    """
    result = {}

    incomes = get_monthly_income()
    expenses = get_monthly_expense()

    total = 0
    for income in incomes:
        income = cast(FinancePlan, income)
        value = income.value if income.value is not None else 0
        total = total + value
    result['income'] = total

    total = 0
    for expense in expenses:
        expense = cast(FinancePlan, expense)
        value = expense.value if expense.value is not None else 0
        total = total + value
    result['expense'] = total

    result['balance'] = result['income'] - result['expense']
    return result


def get_values_for_sensors_pending_monthly() -> dict:
    """
    Retorna valores mensais em aberto:
        - Total receitas a receber
        - Total despesas a pagar
        - diferença = receita - despesa
    """
    result = {}

    incomes = (
        FinancePlan.select().where(
            (FinancePlan.active == 1) &
            (FinancePlan.type == RecordType.RECEITA) &
            (FinancePlan.periodicity == Periodicity.MENSAL)
        )
        .order_by(FinancePlan.day_movement)
    )
    expenses = (
        FinancePlan.select().where(
            (FinancePlan.active == 1) &
            (FinancePlan.type == RecordType.DESPESA) &
            (FinancePlan.periodicity == Periodicity.MENSAL) &
            (FinancePlan.payment_method != PaymentMethod.CARTAO)
        )
        .order_by(FinancePlan.day_movement)
    )

    current_month = datetime.now().month
    transactions = PlanTransaction.select().where(
        PlanTransaction.month == current_month
    )
    transaction_list: list[str] = []
    for t in transactions:
        t = cast(PlanTransaction, t)
        transaction_list.append(t.key())

    total = 0
    for income in incomes:
        income = cast(FinancePlan, income)
        if f'{income.id}-{current_month}' in transaction_list:
            continue
        value = income.value if income.value is not None else 0
        total = total + value

    result['income'] = total

    total = 0
    for expense in expenses:
        expense = cast(FinancePlan, expense)
        if f'{expense.id}-{current_month}' in transaction_list:
            continue
        value = expense.value if expense.value is not None else 0
        total = total + value

    result['expense'] = total

    result['balance'] = result['income'] - result['expense']

    return result


def get_monthly_income() -> [FinancePlan]:
    records = (
        FinancePlan.select().where(
            (FinancePlan.active == 1) &
            (FinancePlan.type == RecordType.RECEITA) &
            (FinancePlan.periodicity == Periodicity.MENSAL)
        )
        .order_by(FinancePlan.day_movement)
    )

    return records


def get_monthly_expense() -> [FinancePlan]:
    records = (
        FinancePlan.select().where(
            (FinancePlan.active == 1) &
            (FinancePlan.type == RecordType.DESPESA) &
            (FinancePlan.periodicity == Periodicity.MENSAL)
        )
        .order_by(FinancePlan.day_movement)
    )

    return records


def get_all_ids_monthly() -> list[int]:
    records = (
        FinancePlan.select().where(
            (FinancePlan.active == 1) &
            (FinancePlan.periodicity == Periodicity.MENSAL)
        )
        .order_by(FinancePlan.day_movement)
    )

    ids = []
    for r in records:
        r = cast(FinancePlan, r)
        ids.append(r.id)

    return ids
