from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant

from .service import get_values_for_sensors_total_monthly, get_values_for_sensors_pending_monthly
from .util import get_device_for_finance_monthly
from ..const import (
    DOMAIN,
    MANAGER
)
from ..util.manager import ObjectManager

_LOGGER = logging.getLogger(__name__)


def get_sensors(hass: HomeAssistant) -> list[Any]:
    entities = []
    manager: ObjectManager = hass.data[DOMAIN][MANAGER]

    monthly_values = get_values_for_sensors_total_monthly()
    monthly_pending_values = get_values_for_sensors_pending_monthly()

    entities.append(MonthlyIncomeSensor(monthly_values['income']))
    entities.append(MonthlyExpenseSensor(monthly_values['expense']))
    entities.append(MonthlyBalanceSensor(monthly_values['balance']))

    entities.append(PendingIncomeSensor(monthly_pending_values['income']))
    entities.append(PendingExpenseSensor(monthly_pending_values['expense']))
    entities.append(PendingBalanceSensor(monthly_pending_values['balance']))

    return entities


class PendingIncomeSensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Receitas Pendentes"
    _attr_icon = "mdi:cash-clock"
    _attr_native_unit_of_measurement = "R$"
    _attr_should_poll = False

    def __init__(self, value: float):
        self._attr_unique_id = "finance_monthly_pending_income"
        self._attr_native_value = value
        self._attr_device_info = get_device_for_finance_monthly()


class PendingExpenseSensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Despesas Pendentes"
    _attr_icon = "mdi:cash-clock"
    _attr_native_unit_of_measurement = "R$"
    _attr_should_poll = False

    def __init__(self, value: float):
        self._attr_unique_id = "finance_monthly_pending_expense"
        self._attr_native_value = value
        self._attr_device_info = get_device_for_finance_monthly()


class PendingBalanceSensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Saldo Pendente"
    _attr_icon = "mdi:scale-balance"
    _attr_native_unit_of_measurement = "R$"
    _attr_should_poll = False

    def __init__(self, value: float):
        self._attr_unique_id = "finance_monthly_pending_balance"
        self._attr_native_value = round(value, 2)
        self._attr_device_info = get_device_for_finance_monthly()


class MonthlyIncomeSensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Receitas Totais"
    _attr_icon = "mdi:cash-plus"
    _attr_native_unit_of_measurement = "R$"
    _attr_should_poll = False

    def __init__(self, total_income: float):
        self._attr_unique_id = "finance_monthly_income_total"
        self._attr_native_value = round(total_income, 2)
        self._attr_device_info = get_device_for_finance_monthly()


class MonthlyExpenseSensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Despesas Totais"
    _attr_icon = "mdi:cash-minus"
    _attr_native_unit_of_measurement = "R$"
    _attr_should_poll = False

    def __init__(self, total_expense: float):
        self._attr_unique_id = "finance_monthly_expense_total"
        self._attr_native_value = round(total_expense, 2)
        self._attr_device_info = get_device_for_finance_monthly()


class MonthlyBalanceSensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Saldo Projetado"
    _attr_icon = "mdi:scale-balance"
    _attr_native_unit_of_measurement = "R$"
    _attr_should_poll = False

    def __init__(self, value: float):
        self._attr_unique_id = "finance_monthly_balance_total"
        self._attr_native_value = round(value, 2)
        self._attr_device_info = get_device_for_finance_monthly()
