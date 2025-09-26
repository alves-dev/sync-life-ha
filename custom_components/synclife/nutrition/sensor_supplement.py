from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant

from .service_supplement import supplements_status_today
from .util import get_device_for_supplement
from ..const import (
    DOMAIN,
    MANAGER,
    NUTRITION_SUPPLEMENT_VALUES
)
from ..util.manager import ObjectManager

_LOGGER = logging.getLogger(__name__)


def get_sensors(hass: HomeAssistant) -> list[Any]:
    entities = []
    manager: ObjectManager = hass.data[DOMAIN][MANAGER]

    values_persons: list[dict] = manager.get_by_key(NUTRITION_SUPPLEMENT_VALUES)
    persons: list[str] = [value['person'] for value in values_persons]
    persons: set[str] = set(persons)

    for person in persons:
        supplements: dict[str, bool] = supplements_status_today(person, hass)
        total = len(supplements)
        intake = sum(supplements.values())

        entities.append(SupplementSummarySensor(person, supplements, f'{intake}/{total}'))

        for supplement, taken in supplements.items():
            entities.append(SupplementIntakeBinarySensor(person, supplement, taken))

    return entities


class SupplementSummarySensor(SensorEntity):

    def __init__(self, person_id: str, attributes: dict, value: str = '0/0'):
        self._attr_unique_id = f"nutrition_supplement_summary_{person_id}"
        self._attr_name = "Intake Summary"
        self._attr_native_value = value
        self._attr_device_info = get_device_for_supplement(person_id)
        self._attr_extra_state_attributes = attributes
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        divided = value.split('/')
        self._all_taken = True if divided[0] == divided[1] else False

    @property
    def icon(self) -> str:
        """Define ícone dinâmico baseado no status."""
        if self._all_taken:
            return "mdi:check-circle-outline"  # completo
        elif self._attr_native_value and self._attr_native_value.startswith("0/"):
            return "mdi:close-circle-outline"  # nenhum ainda
        else:
            return "mdi:progress-check"  # parcial


class SupplementIntakeBinarySensor(BinarySensorEntity):
    """Binary sensor para verificar se a pessoa tomou um suplemento no dia."""

    def __init__(self, person_id: str, supplement: str, taken: bool):
        self._attr_unique_id = f"nutrition_supplement_{person_id}_{supplement}"
        self._attr_name = f"{supplement.capitalize()} Intake"
        self._attr_device_info = get_device_for_supplement(person_id)
        self._attr_is_on = taken

    @property
    def icon(self) -> str:
        if self.is_on:
            return "mdi:check-circle"
        return "mdi:close-circle"
