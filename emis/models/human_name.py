from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
import enum
import json
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
    family_name: str = None
    given: list[str] = field(default_factory=list)
    prefix: list[str] = field(default_factory=list)
    period_start: datetime = None
    period_end: datetime = None


class HumanNameList(db.TypeDecorator):
    impl = db.String

    def process_bind_param(self, value: Any, dialect: Any) -> Any:
        if value is not None:
            return json.dumps(return_as_dict(value))
        return []

    def process_result_value(self, value: Any, dialect: Any) -> Any:
        if value is not None:
            data = json.loads(value)
            for human_name in data:
                if 'use' in human_name:
                    human_name['use'] = HumanNameUse(human_name['use'])
            return [HumanName(**hn) for hn in data]
        return []
