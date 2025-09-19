from datetime import datetime

import voluptuous as vol
from homeassistant.core import ServiceCall

from .model import SleepTracking
from .model_enum import Action
from .service import get_last_event
from ..const import DOMAIN, MANAGER, ENTRY_SLEEP_TRACKING
from ..util.manager import ObjectManager

SLEEP_EVENT_NAME = "sleep_event"


def sleep_event_name_options() -> vol.Schema:
    actions = [Action.SLEEP.value, Action.WAKE_UP.value]

    return vol.Schema(
        {
            vol.Required("person_id"): str,
            vol.Required("action"): vol.In(actions),
        }
    )


async def sleep_event(call: ServiceCall):
    manager: ObjectManager = call.hass.data[DOMAIN][MANAGER]

    person_id: str = call.data["person_id"]
    action: str = call.data["action"]

    if action == Action.SLEEP.value:
        SleepTracking.create(person=person_id, action=Action.SLEEP)
    elif action == Action.WAKE_UP.value:
        last: SleepTracking = get_last_event(person_id)

        computed = False
        minutes = 0
        if last.action == Action.SLEEP:
            minutes = (datetime.now() - last.created_at).total_seconds() // 60
            last.computed = True
            last.save()
            computed = True

        SleepTracking.create(person=person_id, action=Action.WAKE_UP, computed=computed, minutes_slept=minutes)

    entry = manager.get_by_key(ENTRY_SLEEP_TRACKING)
    await call.hass.config_entries.async_reload(entry.entry_id)
