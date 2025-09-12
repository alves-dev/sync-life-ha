import logging
from typing import Any, List

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant

from .service import get_all_supplements_str
from .util import get_device_for_supplement
from ..const import (
    DOMAIN,
    MANAGER,
)
from ..util.manager import ObjectManager

_LOGGER = logging.getLogger(__name__)


def get_selects(hass: HomeAssistant) -> list[Any]:
    entities = []
    manager: ObjectManager = hass.data[DOMAIN][MANAGER]

    names: list[str] = get_all_supplements_str()
    select = SupplementSelect(names)

    entities.append(select)

    return entities


class SupplementSelect(SelectEntity):
    _attr_has_entity_name = True
    _attr_name = "Supplements"
    _attr_icon = "mdi:pill"

    def __init__(self, supplements: List[str]):
        self._attr_unique_id = "nutrition_supplement_select"
        self._attr_options = supplements
        self._attr_current_option = supplements[0] if supplements else None
        self._attr_device_info = get_device_for_supplement()
