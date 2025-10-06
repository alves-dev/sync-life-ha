from datetime import datetime

import voluptuous as vol
from homeassistant.core import ServiceCall

from .model import ExerciseAcademy
from .model_enum import Action
from .service import get_last_event
from ..const import DOMAIN, MANAGER, ENTRY_SLEEP_TRACKING
from ..util.manager import ObjectManager

EXERCISE_ACADEMY_EVENT_NAME = "exercise_academy_event"


def exercise_academy_event_schema() -> vol.Schema:
    actions = [Action.ENTRY.value, Action.EXIT.value]

    return vol.Schema(
        {
            vol.Required("person_id"): str,
            vol.Required("action"): vol.In(actions),
        }
    )


async def exercise_academy_event(call: ServiceCall):
    manager: ObjectManager = call.hass.data[DOMAIN][MANAGER]

    person_id: str = call.data["person_id"]
    action: str = call.data["action"]

    if action == Action.ENTRY.value:
        ExerciseAcademy.create(person=person_id, action=Action.ENTRY)
    elif action == Action.EXIT.value:
        last: ExerciseAcademy = get_last_event(person_id)

        computed = False
        minutes = 0
        if last.action == Action.ENTRY:
            minutes = (datetime.now() - last.created_at).total_seconds() // 60
            last.computed = True
            last.save()
            computed = True

        ExerciseAcademy.create(person=person_id, action=Action.EXIT, computed=computed, minutes_stay=minutes)

    entry = manager.get_by_key(ENTRY_SLEEP_TRACKING)
    await call.hass.config_entries.async_reload(entry.entry_id)
