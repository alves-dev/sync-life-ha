from datetime import datetime, timedelta

from peewee import fn

from .model import SleepTracking
from .model_enum import Action


def is_sleeping(person: str) -> bool:
    """
    Retorna:
    True se a pessoa estiver dormindo,
    False se estiver acordada ou se não houver registros.
    """
    last = (
        SleepTracking
        .select()
        .where(SleepTracking.person == person)
        .order_by(SleepTracking.created_at.desc())
        .first()
    )

    if not last:
        return False  # sem dados

    return last.action == Action.SLEEP


def get_last_sleep_duration(person: str) -> int:
    """
    Retorna o tempo dormido no último WAKE_UP de uma pessoa.
    """
    last_wake_up = (
        SleepTracking
        .select()
        .where(
            (SleepTracking.person == person) &
            (SleepTracking.action == Action.WAKE_UP)
        )
        .order_by(SleepTracking.created_at.desc())
        .first()
    )

    return last_wake_up.minutes_slept if last_wake_up else 0


def get_last_event(person: str) -> SleepTracking:
    return (
        SleepTracking
        .select()
        .where(
            SleepTracking.person == person
        )
        .order_by(SleepTracking.created_at.desc())
        .first()
    )


def get_average_sleep_minutes(person: str, days: int) -> int:
    """Retorna a média de minutos dormidos nos últimos X dias para uma pessoa."""

    since = datetime.now() - timedelta(days=days)

    query = (
        SleepTracking
        .select(fn.AVG(SleepTracking.minutes_slept).alias("avg_minutes"))
        .where(
            (SleepTracking.person == person)
            & (SleepTracking.action == Action.WAKE_UP)
            & (SleepTracking.created_at >= since)
        )
    )

    result = query.dicts().first()
    return int(result["avg_minutes"] or 0)
