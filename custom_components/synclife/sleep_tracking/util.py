from homeassistant.helpers.device_registry import DeviceInfo, DeviceEntryType

from ..const import DOMAIN_SLEEP
from ..util.transforms import person_id_to_str


def get_device_for_sleep(person_id: str) -> DeviceInfo:
    return DeviceInfo(
        identifiers={('sleep_tracking', person_id)},
        name=person_id_to_str(person_id),
        manufacturer=DOMAIN_SLEEP,
        entry_type=DeviceEntryType.SERVICE
    )
