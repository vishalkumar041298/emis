from __future__ import annotations
from dataclasses import dataclass
import enum
import json
from typing import Any
from emis.utils.database import db
from emis.utils.utils import return_as_dict


class ContactPointSystem(enum.Enum):
    PHONE = 'phone'
    FAX = 'fax'
    EMAIL = 'email'
    PAGER = 'pager'
    URL = 'url'
    SMS = 'sms'
    OTHER = 'other'


class ContactPointUse(enum.Enum):
    HOME = 'home'
    WORK = 'work'
    TEMP = 'temp'
    OLD = 'OLD'
    MOBILE = 'mobile'


@dataclass
class ContactPoint:
    system: ContactPointSystem = None
    value: str = None
    use: ContactPointUse = None
    rank: int = None


class ContactPointList(db.TypeDecorator):
    impl = db.JSON

    def process_bind_param(self, value: Any, dialect: Any) -> Any:
        if value is not None:
            return json.dumps(return_as_dict(value))
        return []

    def process_result_value(self, value: Any, dialect: Any) -> Any:
        if value is not None:
            data = json.loads(value)
            for contact_point in data:
                if 'use' in contact_point:
                    contact_point['use'] = ContactPointUse(contact_point['use'])
                if 'system' in contact_point:
                    contact_point['system'] = ContactPointSystem(contact_point['system'])
            return [ContactPoint(**cp) for cp in data]
        return []

    @classmethod
    def prepare_type(cls, items: list[dict[str, Any]]) -> list[ContactPoint]:
        typed_items = []
        for item in items:
            if 'use' in item:
                item['use'] = ContactPointUse(item['use'])
            if 'system' in item:
                item['system'] = ContactPointSystem(item['system'])
            typed_items.append(ContactPoint(**item))
        return typed_items
