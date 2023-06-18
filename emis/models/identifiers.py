from __future__ import annotations
from dataclasses import dataclass
import enum
import json
from typing import Any
from emis.utils.database import db
from emis.utils.utils import return_as_dict


class IdentifierUse(enum.Enum):
    USUAL = 'usual'
    OFFICIAL = 'official'
    TEMP = 'temp'
    SECONDARY = 'secondary'
    OLD = 'old'


@dataclass
class Identifier:
    use: IdentifierUse = None
    system: str = None
    value: str = None
    type: dict = None


class IdentifierList(db.TypeDecorator):
    impl = db.JSON

    def process_bind_param(self, value: Any, dialect: Any) -> Any:
        if value is not None:
            return return_as_dict(value)
        return []

    def process_result_value(self, value: Any, dialect: Any) -> Any:
        if value is not None:
            identifiers_data = json.load(value)
            for identifier in identifiers_data:
                if 'use' in identifier:
                    identifier['use'] = IdentifierUse(identifier['use'])
            return [Identifier(**identifier_data) for identifier_data in identifiers_data]
        return []

    @classmethod
    def prepare_type(cls, items: list[dict[str, Any]]) -> list[Identifier]:
        typed_items = []
        for item in items:
            if 'use' in item:
                item['use'] = IdentifierUse(item['use'])
            typed_items.append(Identifier(**item))
        return typed_items
