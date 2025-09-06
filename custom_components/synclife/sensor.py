import logging
from typing import cast

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNKNOWN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from . import ObjectManager
from .const import (
    DOMAIN,
    MANAGER,
    SENSOR_VEHICLE_MILEAGE,
)
from .vehicle import service as vehicle_service
from .vehicle.model import Vehicle
from .vehicle.util import get_device_by_vehicle

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry,
                            async_add_entities: AddConfigEntryEntitiesCallback) -> None:
    entities = []
    manager: ObjectManager = hass.data[DOMAIN][MANAGER]

    cars = vehicle_service.get_all()
    for car in cars:
        car = cast(Vehicle, car)
        km = vehicle_service.get_last_km_by_vehicle(car)

        sensor = MileageSensor(car, km)
        manager.add(SENSOR_VEHICLE_MILEAGE + str(car.id), sensor)
        entities.append(sensor)

    async_add_entities(entities, update_before_add=True)


class MileageSensor(SensorEntity, RestoreEntity):
    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = "km"
    _attr_name = "Kilometragem"
    _attr_icon = "mdi:road"
    _attr_should_poll = False

    def __init__(self, vehicle: Vehicle, mileage: int):
        self._attr_unique_id = f"vehicle_{vehicle.id}_mileage"
        self._attr_native_value = mileage
        self._attr_device_info = get_device_by_vehicle(vehicle)

    async def async_added_to_hass(self) -> None:
        """This method is called by the Home Assistant when the entity is added"""
        await super().async_added_to_hass()

        last_state = await self.async_get_last_state()
        if last_state is not None and last_state.state != STATE_UNKNOWN:
            try:
                self._attr_native_value = int(last_state.state)
            except ValueError:
                _LOGGER.warning(f"Erro ao restaurar valor '{last_state.state}'")

    def update_mileage(self, value: int) -> None:
        if self.native_value < value:
            self._attr_native_value = value
            self.schedule_update_ha_state()
        else:
            _LOGGER.warning(f"KM atual ({self.native_value}) é maior que o informado: {value}")
