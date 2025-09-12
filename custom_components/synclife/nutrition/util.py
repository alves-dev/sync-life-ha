from homeassistant.helpers.device_registry import DeviceInfo, DeviceEntryType

from ..const import DOMAIN_NUTRITION


def get_device_for_supplement() -> DeviceInfo:
    return DeviceInfo(
        identifiers={('nutrition', 'supplement')},
        name='Supplement',
        manufacturer=DOMAIN_NUTRITION,
        entry_type=DeviceEntryType.SERVICE
    )
