from homeassistant.core import ServiceCall
from homeassistant.helpers import device_registry

from .model import VehicleMileage
from ..const import SENSOR_VEHICLE_MILEAGE, MANAGER, DOMAIN
from ..sensor import MileageSensor
from ..util.manager import ObjectManager

VEHICLE_UPDATE_MILEAGE_NAME = "vehicle_update_mileage"


async def vehicle_update_mileage(call: ServiceCall):
    device_id: str = call.data["device_id"]
    mileage: int = call.data["mileage"]

    registry = device_registry.async_get(call.hass)
    device = registry.async_get(device_id)

    if len(device.identifiers) > 1:
        raise ValueError('Tem mais de 1 identificador')

    _, vehicle_id = next(iter(device.identifiers))

    VehicleMileage.create(vehicle=vehicle_id, mileage=mileage)

    manger: ObjectManager = call.hass.data[DOMAIN][MANAGER]
    sensor_km: MileageSensor = manger.get_by_key(SENSOR_VEHICLE_MILEAGE + str(vehicle_id))

    sensor_km.update_mileage(mileage)
