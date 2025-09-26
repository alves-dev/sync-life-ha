from collections import defaultdict
from datetime import datetime, date

from homeassistant.core import HomeAssistant

from .model import LiquidIntake
from ..const import DOMAIN, MANAGER, NUTRITION_LIQUID_VALUES
from ..util.manager import ObjectManager


def get_all_liquids_str(hass: HomeAssistant) -> list[str]:
    manager: ObjectManager = hass.data[DOMAIN][MANAGER]
    liquids: list[dict] = manager.get_by_key(NUTRITION_LIQUID_VALUES)

    return [value['name'] for value in liquids]


def is_healthy(liquid: str, hass: HomeAssistant) -> bool:
    manager: ObjectManager = hass.data[DOMAIN][MANAGER]
    liquids: list[dict] = manager.get_by_key(NUTRITION_LIQUID_VALUES)

    for l in liquids:
        if l['name'] == liquid:
            return l['healthy']

    return False


def get_liquid_status_today() -> dict[str, dict[str, int]]:
    """
    Retorna ingestão de líquidos de hoje por pessoa.

    Saída:
    {
        "person1": {"healthy": 1200, "unhealthy": 500},
        "person2": {"healthy": 800, "unhealthy": 0},
        ...
    }
    """
    start_of_day = datetime.combine(date.today(), datetime.min.time())

    # Pessoas distintas registradas na base
    persons = [row.person for row in LiquidIntake.select(LiquidIntake.person).distinct()]

    # Inicializa todos com zero
    result: dict[str, dict[str, int]] = {
        person: {"healthy": 0, "unhealthy": 0} for person in persons
    }

    query = (LiquidIntake
             .select()
             .where(LiquidIntake.taken_at >= start_of_day))

    # result: dict[str, dict[str, int]] = defaultdict(lambda: {"healthy": 0, "unhealthy": 0})

    for record in query:
        if record.healthy:
            result[record.person]["healthy"] += record.amount
        else:
            result[record.person]["unhealthy"] += record.amount

    return dict(result)
