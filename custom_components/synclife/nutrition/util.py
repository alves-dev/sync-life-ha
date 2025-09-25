from homeassistant.helpers.device_registry import DeviceInfo, DeviceEntryType

from ..const import DOMAIN_NUTRITION
from ..util.transforms import person_id_to_str


def get_device_for_supplement(person_id: str) -> DeviceInfo:
    return DeviceInfo(
        identifiers={('nutrition_supplement', person_id)},
        name=person_id_to_str(person_id),
        manufacturer=DOMAIN_NUTRITION,
        entry_type=DeviceEntryType.SERVICE
    )
