import logging
import os
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval, async_track_time_change
from peewee import SqliteDatabase

from .const import (
    DOMAIN,
    DB_FILENAME,
    MANAGER,
    DB_INSTANCE,
    CONF_ENTRY_NAME,
    ENTRY_VEHICLES,
    ENTRY_NUTRITION,
    ENTRY_VEHICLES_NAME,
    ENTRY_NUTRITION_NAME,
    NUTRITION_PERSONS,
    ENTRY_FINANCE,
    ENTRY_FINANCE_NAME,
    ENTRY_SLEEP_TRACKING_NAME,
    ENTRY_SLEEP_TRACKING,
    SLEEP_TRACKING_PERSONS,
)
from .database import db_init
from .finance.ha_service import (
    FINANCE_TRANSACTION_MONTHLY_NAME,
    finance_transaction_monthly
)
from .finance.model import init_finance_db
from .nutrition.ha_service import (
    NUTRITION_INTAKE_SUPPLEMENT_NAME,
    nutrition_intake_supplement,
    nutrition_intake_supplement_options
)
from .nutrition.model import init_nutrition_db
from .sleep_tracking.ha_service import SLEEP_EVENT_NAME, sleep_event_name_options, sleep_event
from .sleep_tracking.model import init_sleep_db
from .util.manager import ObjectManager
from .vehicle.ha_service import VEHICLE_UPDATE_MILEAGE_NAME, vehicle_update_mileage
from .vehicle.model import init_vehicle_db, Vehicle
from .vehicle.service import update_vehicle_maintenances

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR, Platform.SELECT]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    manager = ObjectManager()
    if MANAGER not in hass.data[DOMAIN]:
        hass.data[DOMAIN][MANAGER] = manager

    # ----- Values from configuration.yaml ----- #
    persons = config.get(DOMAIN, {}).get('nutrition', {}).get('persons', [])
    manager.add(NUTRITION_PERSONS, persons)

    persons = config.get(DOMAIN, {}).get('sleep_tracking', {}).get('persons', [])
    manager.add(SLEEP_TRACKING_PERSONS, persons)
    # ----- Values from configuration.yaml ----- #

    # ----- Database config ----- #
    db_path = hass.config.path(f".storage/{DB_FILENAME}")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    def setup_orm():
        db: SqliteDatabase = db_init(db_path)
        manager: ObjectManager = hass.data[DOMAIN][MANAGER]
        manager.add(DB_INSTANCE, db)
        init_vehicle_db(db)
        init_nutrition_db(db)
        init_finance_db(db)
        init_sleep_db(db)

    await hass.async_add_executor_job(setup_orm)
    # ----- Database config ----- #

    # ----- Services registry ----- #
    hass.services.async_register(
        domain=DOMAIN,
        service=VEHICLE_UPDATE_MILEAGE_NAME,
        service_func=vehicle_update_mileage
    )

    hass.services.async_register(
        domain=DOMAIN,
        service=NUTRITION_INTAKE_SUPPLEMENT_NAME,
        service_func=nutrition_intake_supplement,
        schema=nutrition_intake_supplement_options()
    )

    hass.services.async_register(
        domain=DOMAIN,
        service=FINANCE_TRANSACTION_MONTHLY_NAME,
        service_func=finance_transaction_monthly
    )

    hass.services.async_register(
        domain=DOMAIN,
        service=SLEEP_EVENT_NAME,
        service_func=sleep_event,
        schema=sleep_event_name_options()
    )

    # ----- Services registry ----- #

    # ----- background function ----- #
    async def _periodic_update(now):
        await update_vehicle_maintenances(hass)

    async def _daily_midnight_update(now):
        await async_reload_all_entries(hass)

    async_track_time_interval(hass, _periodic_update, timedelta(hours=12))
    async_track_time_change(hass, _daily_midnight_update, hour=0, minute=1, second=0, )
    # ----- background function ----- #

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    manager: ObjectManager = hass.data[DOMAIN][MANAGER]

    entry_name = entry.data.get(CONF_ENTRY_NAME, None)
    if entry_name == ENTRY_VEHICLES_NAME:
        manager.add(ENTRY_VEHICLES, entry)
    elif entry_name == ENTRY_NUTRITION_NAME:
        manager.add(ENTRY_NUTRITION, entry)
    elif entry_name == ENTRY_FINANCE_NAME:
        manager.add(ENTRY_FINANCE, entry)
    elif entry_name == ENTRY_SLEEP_TRACKING_NAME:
        manager.add(ENTRY_SLEEP_TRACKING, entry)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return unload_ok


async def async_reload_all_entries(hass: HomeAssistant) -> None:
    """
    Reset as 00:00
    """
    manager: ObjectManager = hass.data[DOMAIN][MANAGER]

    entry = manager.get_by_key(ENTRY_VEHICLES)
    await hass.config_entries.async_reload(entry.entry_id)

    entry = manager.get_by_key(ENTRY_NUTRITION)
    await hass.config_entries.async_reload(entry.entry_id)

    entry = manager.get_by_key(ENTRY_FINANCE)
    await hass.config_entries.async_reload(entry.entry_id)
