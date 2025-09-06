from homeassistant.helpers.device_registry import DeviceInfo, DeviceEntryType

from ..vehicle.model import Vehicle
from ..const import DOMAIN_VEHICLE


def get_device_by_vehicle(vehicle: Vehicle) -> DeviceInfo:
    return DeviceInfo(
        identifiers={('vehicle_id', vehicle.id)},
        name=vehicle.name,
        manufacturer=vehicle.brand,
        model=vehicle.model,
        sw_version=DOMAIN_VEHICLE,
        serial_number=vehicle.plate,
        entry_type=DeviceEntryType.SERVICE
    )
