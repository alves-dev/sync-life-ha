import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_ENTRY_NAME
from .vehicle.sensor import get_sensors as vehicle_get_sensors

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry,
                            async_add_entities: AddConfigEntryEntitiesCallback) -> None:
    entities = []
    entry_name = entry.data.get(CONF_ENTRY_NAME, None)
    if entry_name == 'Veículos':
        entities = vehicle_get_sensors(hass)

    async_add_entities(entities, update_before_add=True)
