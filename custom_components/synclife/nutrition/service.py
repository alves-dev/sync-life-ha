from datetime import date

from homeassistant.core import HomeAssistant
from peewee import fn

from .model import SupplementIntake
from ..const import NUTRITION_VALUES, DOMAIN, MANAGER
from ..util.manager import ObjectManager


def get_all_supplements_str(hass: HomeAssistant) -> list[str]:
    manager: ObjectManager = hass.data[DOMAIN][MANAGER]
    values_persons: list[dict] = manager.get_by_key(NUTRITION_VALUES)

    return [value['supplement'] for value in values_persons]


def supplements_status_today(person_id: str, hass: HomeAssistant) -> dict[str, bool]:
    today = date.today()
    supplements = []

    manager: ObjectManager = hass.data[DOMAIN][MANAGER]
    values_persons: list[dict] = manager.get_by_key(NUTRITION_VALUES)

    for value in values_persons:
        if value['person'] == person_id:
            supplements.append(value['supplement'])

    results = {}
    for supplement in supplements:
        taken = (
            SupplementIntake
            .select()
            .where(
                (SupplementIntake.person == person_id) &
                (SupplementIntake.supplement == supplement) &
                (fn.DATE(SupplementIntake.taken_at) == today)
            )
            .exists()
        )
        results[supplement] = taken

    return results
