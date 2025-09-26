import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import (
    CONF_ENTRY_NAME,
    ENTRY_VEHICLES_NAME,
    ENTRY_NUTRITION_NAME,
    ENTRY_FINANCE_NAME,
    ENTRY_SLEEP_TRACKING_NAME,
)
from .finance.sensor import get_sensors as finance_get_sensors
from .nutrition.sensor_liquid import get_sensors as nutrition_liquid_get_sensors
from .nutrition.sensor_supplement import get_sensors as nutrition_supplement_get_sensors
from .sleep_tracking.sensor import get_sensors as sleep_get_sensors
from .vehicle.sensor import get_sensors as vehicle_get_sensors

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry,
                            async_add_entities: AddConfigEntryEntitiesCallback) -> None:
    entities = []
    entry_name = entry.data.get(CONF_ENTRY_NAME, None)

    if entry_name == ENTRY_VEHICLES_NAME:
        entities = vehicle_get_sensors(hass)

    if entry_name == ENTRY_NUTRITION_NAME:
        entities = nutrition_supplement_get_sensors(hass)
        entities.extend(nutrition_liquid_get_sensors(hass))

    if entry_name == ENTRY_FINANCE_NAME:
        entities = finance_get_sensors(hass)

    if entry_name == ENTRY_SLEEP_TRACKING_NAME:
        entities = sleep_get_sensors(hass)

    async_add_entities(entities, update_before_add=True)
