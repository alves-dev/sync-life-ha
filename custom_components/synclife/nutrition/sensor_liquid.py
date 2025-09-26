from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.core import HomeAssistant

from .service_liquid import get_liquid_status_today
from .util import get_device_for_liquid
from ..const import NUTRITION_LIQUID_GOALS, MANAGER, DOMAIN
from ..util.manager import ObjectManager

_LOGGER = logging.getLogger(__name__)


def get_sensors(hass: HomeAssistant) -> list[Any]:
    entities = []
    manager: ObjectManager = hass.data[DOMAIN][MANAGER]

    liquid_goals: list[dict] = manager.get_by_key(NUTRITION_LIQUID_GOALS)
    for goal in liquid_goals:
        entities.append(LiquidGoalSensor(goal["person"], goal["name"], goal["value"]))

    liquid_status: dict[str, dict[str, int]] = get_liquid_status_today()
    for person, values in liquid_status.items():
        healthy_amount = values.get("healthy", 0)
        unhealthy_amount = values.get("unhealthy", 0)

        entities.append(HealthyLiquidIntakeSensor(person, healthy_amount))
        entities.append(UnhealthyLiquidIntakeSensor(person, unhealthy_amount))

    return entities


class AbstractLiquidSensor(SensorEntity):
    """Base para sensores de ingestão de líquidos."""

    _attr_device_class = SensorDeviceClass.VOLUME
    _attr_native_unit_of_measurement = "ml"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_suggested_display_precision = 0


class HealthyLiquidIntakeSensor(AbstractLiquidSensor):
    """Quantidade de líquidos saudáveis ingeridos hoje."""

    def __init__(self, person: str, amount: int):
        self._attr_unique_id = f"liquid_healthy_{person}"
        self._attr_name = "Healthy Liquid Intake"
        self._attr_native_value = amount
        self._attr_device_info = get_device_for_liquid(person)
        self._attr_icon = "mdi:cup-water"


class UnhealthyLiquidIntakeSensor(AbstractLiquidSensor):
    """Quantidade de líquidos não saudáveis ingeridos hoje."""

    def __init__(self, person: str, amount: int):
        self._attr_unique_id = f"liquid_unhealthy_{person}"
        self._attr_name = "Unhealthy Liquid Intake"
        self._attr_native_value = amount
        self._attr_device_info = get_device_for_liquid(person)
        self._attr_icon = "mdi:cup-off"


class LiquidGoalSensor(SensorEntity):
    """Sensor que representa uma meta"""

    def __init__(self, person: str, goal_name: str, value: int):
        self._attr_name = goal_name
        self._attr_unique_id = f"liquid_goal_{person}_{goal_name}"
        self._attr_native_unit_of_measurement = "ml"
        self._attr_native_value = value
        self._attr_device_info = get_device_for_liquid(person)
        self._attr_icon = "mdi:alpha-m-circle"
