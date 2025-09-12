from datetime import date

from peewee import fn

from .model import Supplement, SupplementIntake


def get_all_supplements_str() -> list[str]:
    supplements = Supplement.select()
    return [s.name for s in supplements]


def get_supplement_by_name(supplement: str) -> Supplement:
    return Supplement.select().where(
        Supplement.name == supplement
    ).first()


def supplements_status_today(person_name: str) -> dict[str, bool]:
    today = date.today()

    results = {}
    for s in Supplement.select():
        taken = (
            SupplementIntake
            .select()
            .where(
                (SupplementIntake.person == person_name) &
                (SupplementIntake.supplement == s) &
                (fn.DATE(SupplementIntake.taken_at) == today)
            )
            .exists()
        )
        results[s.name] = taken

    return results
