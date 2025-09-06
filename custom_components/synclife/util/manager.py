import logging
from typing import Optional, Dict

_LOGGER = logging.getLogger(__name__)


class ObjectManager:
    _instance: Optional["ObjectManager"] = None
    _objects: Dict[str, any] = {}

    def __new__(cls):
        """Implementa o padrão Singleton."""
        if cls._instance is None:
            cls._instance = super(ObjectManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True

    @classmethod
    def instance(cls) -> "ObjectManager":
        return cls()

    def add(self, key: str, obj: any) -> None:
        self._objects[key] = obj
        _LOGGER.debug(f"'{key}' added")

    def get_by_key(self, key: str) -> Optional[any]:
        if key in self._objects:
            return self._objects[key]
        _LOGGER.warning(f"'{key}' not found in objects!")
        return None
