import logging
from datetime import datetime
from typing import cast, Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import STATE_UNKNOWN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util import dt as dt_util

from . import service
from .model import VehicleMileage, Vehicle, VehicleMaintenance
from .util import get_device_by_vehicle
from ..const import (
    DOMAIN,
    MANAGER,
    SENSOR_VEHICLE_MILEAGE,
    SENSOR_VEHICLE_MILEAGE_UPDATE,
    SENSOR_VEHICLE_UPDATE,
)
from ..util.manager import ObjectManager

_LOGGER = logging.getLogger(__name__)


def get_sensors(hass: HomeAssistant) -> list[Any]:
    entities = []
    manager: ObjectManager = hass.data[DOMAIN][MANAGER]

    cars = service.get_all()
    for car in cars:
        car = cast(Vehicle, car)
        mileage: VehicleMileage = service.get_last_km_by_vehicle(car)

        sensor_mileage = MileageSensor(car, mileage)
        sensor_mileage_date = MileageUpdateSensor(car, mileage)
        sensor_vehicle_date = VehicleUpdateSensor(car, mileage)

        manager.add(SENSOR_VEHICLE_MILEAGE + str(car.id), sensor_mileage)
        manager.add(SENSOR_VEHICLE_MILEAGE_UPDATE + str(car.id), sensor_mileage_date)
        manager.add(SENSOR_VEHICLE_UPDATE + str(car.id), sensor_vehicle_date)

        entities.append(sensor_mileage)
        entities.append(sensor_mileage_date)
        entities.append(sensor_vehicle_date)

    # Sensors maintenance
    for car in cars:
        needs = False
        pending = []
        for m in car.maintenances:
            maintenance: VehicleMaintenance = cast(VehicleMaintenance, m)
            entities.append(MaintenanceSensor(car, maintenance))

            if maintenance.bool_required:
                needs = True
                pending.append(maintenance.type)

        entities.append(VehicleNeedsMaintenanceSensor(car, needs, pending))

    return entities


class MileageSensor(SensorEntity, RestoreEntity):
    _attr_has_entity_name = True
    _attr_native_unit_of_measurement = "km"
    _attr_name = "Mileage"
    _attr_icon = "mdi:road"
    _attr_should_poll = False

    def __init__(self, vehicle: Vehicle, mileage: VehicleMileage):
        self._attr_unique_id = f"vehicle_{vehicle.id}_mileage"
        self._attr_native_value = mileage.mileage if mileage else None
        self._attr_device_info = get_device_by_vehicle(vehicle)
        self._mileage_id = mileage.id if mileage else None

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

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Atributos extras mostrados no HA."""
        return {
            "mileage_id": self._mileage_id
        }


class MileageUpdateSensor(SensorEntity, RestoreEntity):
    """Sensor somente leitura para armazenar uma data/hora."""

    _attr_has_entity_name = True
    _attr_name = "Last Update Mileage"
    _attr_icon = "mdi:clock"
    _attr_should_poll = False
    _attr_device_class = "timestamp"

    def __init__(self, vehicle: Vehicle, mileage: VehicleMileage):
        self._attr_unique_id = f"vehicle_{vehicle.id}_mileage_last_update"
        self._attr_native_value: datetime | None = (
            dt_util.as_local(mileage.created_at) if mileage else None
        )
        self._attr_device_info = get_device_by_vehicle(vehicle)

    def async_set_datetime(self):
        """Atualiza a data/hora do sensor."""
        self._attr_native_value = dt_util.utcnow()
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """Restaura último valor após reinício do HA."""
        await super().async_added_to_hass()

        last_state = await self.async_get_last_state()
        if last_state is None or last_state.state in ("unknown", "unavailable"):
            _LOGGER.warning("Não foi possível restaurar datetime anterior")
            return

        restored = dt_util.parse_datetime(last_state.state)
        if restored is None:
            _LOGGER.warning("Não foi possível converter a data")
            return

        self._attr_native_value = restored


class VehicleUpdateSensor(SensorEntity, RestoreEntity):
    """Sensor somente leitura para armazenar uma data/hora."""

    _attr_has_entity_name = True
    _attr_name = "Last Update"
    _attr_icon = "mdi:clock"
    _attr_should_poll = False
    _attr_device_class = "timestamp"

    def __init__(self, vehicle: Vehicle, mileage: VehicleMileage):
        self._attr_unique_id = f"vehicle_{vehicle.id}_vehicle_last_update"
        self._attr_native_value: datetime | None = (
            dt_util.as_local(mileage.created_at) if mileage else None
        )
        self._attr_device_info = get_device_by_vehicle(vehicle)

    def async_set_datetime(self):
        """Atualiza a data/hora do sensor."""
        self._attr_native_value = dt_util.utcnow()
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        """Restaura último valor após reinício do HA."""
        await super().async_added_to_hass()

        last_state = await self.async_get_last_state()
        if last_state is None or last_state.state in ("unknown", "unavailable"):
            _LOGGER.warning("Não foi possível restaurar datetime anterior")
            return

        restored = dt_util.parse_datetime(last_state.state)
        if restored is None:
            _LOGGER.warning("Não foi possível converter a data")
            return

        self._attr_native_value = restored


class MaintenanceSensor(SensorEntity):
    """Sensor genérico para manutenção de veículo."""

    _attr_has_entity_name = True
    _attr_should_poll = False
    _attr_icon = "mdi:wrench"

    def __init__(self, vehicle: Vehicle, maintenance: VehicleMaintenance) -> None:
        self.vehicle = vehicle
        self.maintenance = maintenance

        self._attr_unique_id = f"vehicle_{vehicle.id}_maintenance_{maintenance.type}"
        self._attr_name = f"{vehicle.name} {maintenance.type.replace('_', ' ').title()}"
        self._attr_native_unit_of_measurement = "%" if maintenance.percentage is not None else None
        self._attr_native_value = maintenance.percentage or 0
        self._attr_device_info = get_device_by_vehicle(vehicle)

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Atributos extras com informações de manutenção."""
        return {
            "type": self.maintenance.type,
            "last_date": self.maintenance.last_date.isoformat() if self.maintenance.last_date else None,
            "last_mileage": self.maintenance.last_mileage,
            "next_date": self.maintenance.next_date.isoformat() if self.maintenance.next_date else None,
            "next_mileage": self.maintenance.next_mileage,
            "required": self.maintenance.bool_required,
            "note": self.maintenance.note,
        }

    # def update_maintenance(self, percentage: float) -> None:
    #     """Atualiza o percentual da manutenção."""
    #     self._attr_native_value = percentage
    #     self.schedule_update_ha_state()


class VehicleNeedsMaintenanceSensor(BinarySensorEntity):
    """Sensor binário que indica se o veículo precisa de manutenção."""

    _attr_has_entity_name = True
    _attr_should_poll = False
    _attr_device_class = "problem"
    _attr_icon = "mdi:car-wrench"

    def __init__(self, vehicle: Vehicle, needs: bool, pending: list[str]) -> None:
        self.vehicle = vehicle
        self._pending = pending
        self._attr_unique_id = f"vehicle_{vehicle.id}_needs_maintenance"
        self._attr_name = f"{vehicle.name} Needs Maintenance"
        self._attr_device_info = get_device_by_vehicle(vehicle)
        self._attr_is_on = needs

    @property
    def extra_state_attributes(self) -> dict[str, any]:
        """Lista quais manutenções estão pendentes."""
        return {"pending": self._pending}
