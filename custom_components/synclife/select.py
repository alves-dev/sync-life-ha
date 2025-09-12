import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_ENTRY_NAME, ENTRY_NUTRITION_NAME
from .nutrition.select import get_selects as nutrition_get_selects

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry,
                            async_add_entities: AddConfigEntryEntitiesCallback) -> None:
    entities = []
    entry_name = entry.data.get(CONF_ENTRY_NAME, None)
    if entry_name == ENTRY_NUTRITION_NAME:
        entities = nutrition_get_selects(hass)

    async_add_entities(entities, update_before_add=True)
