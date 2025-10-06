from .model import ExerciseAcademy


def get_last_event(person: str) -> ExerciseAcademy:
    return (
        ExerciseAcademy
        .select()
        .where(
            ExerciseAcademy.person == person
        )
        .order_by(ExerciseAcademy.created_at.desc())
        .first()
    )
