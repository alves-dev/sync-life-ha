from homeassistant.helpers.device_registry import DeviceInfo, DeviceEntryType

from ..const import DOMAIN_FINANCE


def get_device_for_finance_monthly() -> DeviceInfo:
    return DeviceInfo(
        identifiers={('finance', 'mensal')},
        name='Mensal',
        manufacturer=DOMAIN_FINANCE,
        entry_type=DeviceEntryType.SERVICE
    )
