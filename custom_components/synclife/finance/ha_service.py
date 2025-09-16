from datetime import datetime

from homeassistant.auth.models import User
from homeassistant.core import ServiceCall

from .model import PlanTransaction
from ..const import DOMAIN, MANAGER, ENTRY_FINANCE
from ..util.manager import ObjectManager

FINANCE_TRANSACTION_MONTHLY_NAME = "finance_transaction_monthly"


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
