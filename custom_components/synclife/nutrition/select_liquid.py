import logging
from typing import Any, List

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant

from .service_liquid import get_all_liquids_str
from .util import get_device_for_liquid

_LOGGER = logging.getLogger(__name__)


def get_selects(hass: HomeAssistant) -> list[Any]:
    entities = []

    liquid_names: list[str] = get_all_liquids_str(hass)
    select = LiquidSelect(liquid_names)
    entities.append(select)

    return entities


class LiquidSelect(SelectEntity):
    _attr_has_entity_name = True
    _attr_name = "Liquid options"
    _attr_icon = "mdi:beer"

    def __init__(self, liquids: List[str]):
        self._attr_unique_id = "liquid_options_select"
        self._attr_options = liquids
        self._attr_current_option = liquids[0] if liquids else None
        self._attr_device_info = get_device_for_liquid('person.liquid_geral')

    async def async_select_option(self, option: str) -> None:
        """Define a opção selecionada."""
        if option not in self._attr_options:
            raise ValueError(f"Opção inválida: {option}")
        self._attr_current_option = option
        self.async_write_ha_state()
