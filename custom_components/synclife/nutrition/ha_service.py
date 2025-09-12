import voluptuous as vol
from homeassistant.core import ServiceCall

from .model import SupplementIntake, Supplement
from .service import get_all_supplements_str, get_supplement_by_name
from ..const import DOMAIN, MANAGER, ENTRY_NUTRITION
from ..util.manager import ObjectManager

NUTRITION_INTAKE_SUPPLEMENT_NAME = "nutrition_intake_supplement"


def nutrition_intake_supplement_options() -> vol.Schema:
    names = get_all_supplements_str()

    return vol.Schema(
        {
            vol.Required("person_id"): str,
            vol.Required("supplement"): vol.In(names),
        }
    )


async def nutrition_intake_supplement(call: ServiceCall):
    manager: ObjectManager = call.hass.data[DOMAIN][MANAGER]

    person_id: str = call.data["person_id"]
    supplement: str = call.data["supplement"]

    model: Supplement = get_supplement_by_name(supplement)

    SupplementIntake.create(person=person_id, supplement=model.id, amount_grams=model.dose_grams)

    entry = manager.get_by_key(ENTRY_NUTRITION)
    await call.hass.config_entries.async_reload(entry.entry_id)
