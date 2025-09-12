from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant

from .service import supplements_status_today
from .util import get_device_for_supplement
from ..const import (
    DOMAIN,
    MANAGER,
    NUTRITION_PERSONS
)
from ..util.manager import ObjectManager

_LOGGER = logging.getLogger(__name__)


def get_sensors(hass: HomeAssistant) -> list[Any]:
    entities = []
    manager: ObjectManager = hass.data[DOMAIN][MANAGER]

    persons = manager.get_by_key(NUTRITION_PERSONS)

    for person in persons:
        supplements: dict[str, bool] = supplements_status_today(person)
        total = len(supplements)
        intake = sum(supplements.values())

        entities.append(SupplementSummarySensor(person, supplements, f'{intake}/{total}'))

    return entities


class SupplementSummarySensor(SensorEntity):

    def __init__(self, person_id: str, attributes: dict, value: str = '0/0'):
        self._attr_unique_id = f"nutrition_supplement_summary_{person_id}"
        self._attr_name = f"Supplement Intake {person_id.split('.')[-1].title()}"
        self._attr_native_value = value
        self._attr_device_info = get_device_for_supplement()
        self._attr_extra_state_attributes = attributes
        divided = value.split('/')
        self._all_taken = True if divided[0] == divided[1] else False

    @property
    def icon(self) -> str:
        """Define ícone dinâmico baseado no status."""
        if self._all_taken:
            return "mdi:check-circle-outline"  # verde
        elif self._attr_native_value and self._attr_native_value.startswith("0/"):
            return "mdi:close-circle-outline"  # nenhum ainda
        else:
            return "mdi:progress-check"  # parcial
