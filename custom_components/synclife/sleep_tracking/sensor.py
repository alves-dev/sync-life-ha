from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant

from .service import is_sleeping, get_last_sleep_duration, get_average_sleep_minutes
from .util import get_device_for_sleep
from ..const import (
    DOMAIN,
    MANAGER,
    SLEEP_TRACKING_PERSONS
)
from ..util.manager import ObjectManager
from ..util.transforms import person_id_to_str

_LOGGER = logging.getLogger(__name__)

AVERAGE_DAYS = 5


def get_sensors(hass: HomeAssistant) -> list[Any]:
    entities = []
    manager: ObjectManager = hass.data[DOMAIN][MANAGER]

    persons = manager.get_by_key(SLEEP_TRACKING_PERSONS)

    someone_sleeping = False
    for person in persons:
        sleeping: bool = is_sleeping(person)
        minutes: int = get_last_sleep_duration(person)
        average: int = get_average_sleep_minutes(person, AVERAGE_DAYS)

        someone_sleeping = True if sleeping else False

        entities.append(SleepBinarySensor(person, sleeping))
        entities.append(LastSleepDurationSensor(person, minutes))
        entities.append(AverageSleepDurationSensor(person, average, AVERAGE_DAYS))

    #TODO: sensor indicando horario médio que vai dormir e que acorda

    entities.append(SleepBinarySensor('person.geral', someone_sleeping))

    return entities


class SleepBinarySensor(BinarySensorEntity):
    def __init__(self, person: str, sleeping: bool):
        self._attr_name = f"{person_id_to_str(person)} is sleeping"
        self._attr_unique_id = f"sleeping_{person.lower()}"
        self._is_sleeping = sleeping
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_device_class = "occupancy"
        self._attr_device_info = get_device_for_sleep(person)

    @property
    def icon(self) -> str:
        """Define um ícone customizado dependendo do estado."""
        if self._is_sleeping:
            return "mdi:sleep"  # dormindo
        return "mdi:sleep-off"  # acordado

    @property
    def is_on(self) -> bool:
        """True if the person is sleeping."""
        return self._is_sleeping


def calculate_native_value(minutes: int):
    td = timedelta(minutes=minutes)
    hours, remainder = divmod(td.seconds, 3600)
    minutes = remainder // 60
    return f"{hours}:{minutes:02d}"


class LastSleepDurationSensor(SensorEntity):
    """Sensor que mostra a duração do último sono em horas e minutos."""

    def __init__(self, person: str, minutes: int):
        self._minutes = minutes
        self._attr_name = f"{person_id_to_str(person)} Last Sleep Duration"
        self._attr_unique_id = f"{person}_last_sleep_duration"
        self._attr_icon = "mdi:bed-clock"
        self._attr_native_value = calculate_native_value(minutes)
        self._attr_device_info = get_device_for_sleep(person)

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Atributos extras mostrados no HA."""
        return {
            "minutes": self._minutes
        }


class AverageSleepDurationSensor(SensorEntity):
    """Sensor que mostra a média de duração de sono de X dias."""

    def __init__(self, person: str, minutes: int, days: int):
        self._minutes = minutes
        self._days = days
        self._attr_name = f"{person_id_to_str(person)} Average Duration"
        self._attr_unique_id = f"{person}_average_sleep_duration_{days}"
        self._attr_icon = "mdi:bed-clock"
        self._attr_native_value = calculate_native_value(minutes)
        self._attr_device_info = get_device_for_sleep(person)

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Atributos extras mostrados no HA."""
        return {
            "minutes": self._minutes,
            "days": self._days,
        }
