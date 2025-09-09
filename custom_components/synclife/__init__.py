import logging
import os
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval
from peewee import SqliteDatabase

from .const import DOMAIN, DB_FILENAME, MANAGER, DB_INSTANCE, CONF_ENTRY_NAME, ENTRY_VEHICLES
from .database import db_init
from .util.manager import ObjectManager
from .vehicle.ha_service import VEHICLE_UPDATE_MILEAGE_NAME, vehicle_update_mileage
from .vehicle.model import init_vehicle_db, Vehicle
from .vehicle.service import update_vehicle_maintenances

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    if MANAGER not in hass.data[DOMAIN]:
        hass.data[DOMAIN][MANAGER] = ObjectManager()

    db_path = hass.config.path(f".storage/{DB_FILENAME}")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    def setup_orm():
        db: SqliteDatabase = db_init(db_path)
        manager: ObjectManager = hass.data[DOMAIN][MANAGER]
        manager.add(DB_INSTANCE, db)
        init_vehicle_db(db)

    await hass.async_add_executor_job(setup_orm)

    # Services registry
    hass.services.async_register(
        domain=DOMAIN,
        service=VEHICLE_UPDATE_MILEAGE_NAME,
        service_func=vehicle_update_mileage
    )

    async def _periodic_update(now):
        await update_vehicle_maintenances(hass)

    async_track_time_interval(hass, _periodic_update, timedelta(hours=12))

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    manager: ObjectManager = hass.data[DOMAIN][MANAGER]

    entry_name = entry.data.get(CONF_ENTRY_NAME, None)
    if entry_name == 'Veículos':
        manager.add(ENTRY_VEHICLES, entry)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return unload_ok
