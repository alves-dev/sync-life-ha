from datetime import datetime

import voluptuous as vol
from homeassistant.auth.models import User
from homeassistant.core import ServiceCall

from .model import PlanTransaction
from .service import get_all_ids_monthly
from ..const import DOMAIN, MANAGER, ENTRY_FINANCE
from ..util.manager import ObjectManager

FINANCE_TRANSACTION_MONTHLY_NAME = "finance_transaction_monthly"


def finance_transaction_monthly_schema() -> vol.Schema:
    ids = get_all_ids_monthly()

    return vol.Schema(
        {
            vol.Required("plan_id"): vol.In(ids),
        }
    )


async def finance_transaction_monthly(call: ServiceCall):
    manager: ObjectManager = call.hass.data[DOMAIN][MANAGER]

    plan_id: str = call.data["plan_id"]
    current_month = datetime.now().month
    username = 'unknown'

    user: User = await call.hass.auth.async_get_user(call.context.user_id)
    if user:
        username = user.name

    PlanTransaction.create(id_finance_plan=plan_id, month=current_month, person_id=username)

    entry = manager.get_by_key(ENTRY_FINANCE)
    await call.hass.config_entries.async_reload(entry.entry_id)
