from datetime import datetime

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.core import ServiceCall, HomeAssistant

from .model import SupplementIntake
from .service import get_all_supplements_str
from ..const import DOMAIN, MANAGER, ENTRY_NUTRITION
from ..util.manager import ObjectManager

NUTRITION_INTAKE_SUPPLEMENT_NAME = "nutrition_intake_supplement"


def nutrition_intake_supplement_options(hass: HomeAssistant) -> vol.Schema:
    names: list[str] = get_all_supplements_str(hass)

    return vol.Schema(
        {
            vol.Required("person_id"): str,
            vol.Required("supplement"): vol.In(names),
            vol.Required("amount"): int,
            vol.Optional("taken_at"): cv.datetime
        }
    )


async def nutrition_intake_supplement(call: ServiceCall):
    manager: ObjectManager = call.hass.data[DOMAIN][MANAGER]

    person_id: str = call.data["person_id"]
    supplement: str = call.data["supplement"]
    amount: int = call.data["amount"]
    taken_at: datetime = call.data.get('taken_at', datetime.now())

    SupplementIntake.create(person=person_id, supplement=supplement, amount=amount, taken_at=taken_at)

    entry = manager.get_by_key(ENTRY_NUTRITION)
    await call.hass.config_entries.async_reload(entry.entry_id)
