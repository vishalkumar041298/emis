from dataclasses import is_dataclass
from enum import Enum
from typing import Any


def remove_urn(id: str) -> str:
    if 'urn:uuid:' in id:
        return id.split(":")[-1]
    return id


def return_as_dict(obj: Any, type: Any = None) -> Any:
    if isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, list):
        return [return_as_dict(v) for v in obj]
    elif is_dataclass(obj) or (type and isinstance(obj, type)):
        return {key: return_as_dict(value) for key, value in obj.__dict__.items()}
    return obj
