from __future__ import annotations
from dataclasses import dataclass, field
import enum
from typing import Any
from emis.utils.database import db
from emis.utils.utils import return_as_dict


class HumanNameUse(enum.Enum):
    USUAL = 'usual'
    OFFICIAL = 'official'
    TEMP = 'temp'
    NICKNAME = 'nickname'
    ANONYMOUS = 'anonymous'
    OLD = 'old'
    MAIDEN = 'maiden'


@dataclass
class HumanName:
    use: HumanNameUse = None
    text: str = None
    family: str = None
    given: list[str] = field(default_factory=list)
    prefix: list[str] = field(default_factory=list)
    suffix: list[str] = field(default_factory=list)


class HumanNameList(db.TypeDecorator):
    impl = db.JSON

    def process_bind_param(self, value: Any, dialect: Any) -> Any:
        if value is not None:
            return return_as_dict(value)
        return []

    def process_result_value(self, value: Any, dialect: Any) -> Any:
        if value is not None:
            # data = json.loads(value)
            for human_name in value:
                if human_name.get('use'):
                    human_name['use'] = HumanNameUse(human_name['use'])
            return [HumanName(**hn) for hn in value]
        return []

    @classmethod
    def prepare_type(cls, items: list[dict[str, Any]]) -> list[HumanName]:
        typed_items = []
        for item in items:
            if 'use' in item:
                item['use'] = HumanNameUse(item['use'])
            typed_items.append(HumanName(**item))
        return typed_items
