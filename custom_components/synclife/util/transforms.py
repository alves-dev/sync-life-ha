def person_id_to_str(person_id: str) -> str:
    p: list = person_id.split('.')
    name: str = p[-1]
    name = name.replace('_', ' ')
    return name.title()
