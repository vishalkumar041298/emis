from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass
import enum
import json
from typing import Any
from sqlalchemy import Enum
from emis.utils.database import db
from emis.utils.utils import JSONSerializableMixin


class IdentifierUse(enum.Enum):
    USUAL = 'usual'
    OFFICIAL = 'official'
    TEMP = 'temp'
    SECONDARY = 'secondary'
    OLD = 'old'


class Identifier(db.Model, JSONSerializableMixin):
    id = db.Column(db.String(64), primary_key=True)
    use = db.Column(Enum(IdentifierUse))
    type = db.Column(db.JSON)
    system = db.Column(db.String(128))
    value = db.Column(db.String(128))
    patient_id = db.Column(db.String(64), db.ForeignKey('patient.id'))
    observation_id = db.Column(db.String(64), db.ForeignKey('observation.id'))
    encounter_id = db.Column(db.String(64), db.ForeignKey('encounter.id'))

    @classmethod
    def prepare_model(cls, obj: dict) -> Identifier:

        pass
        # birth_date = None
        # deceased_date_time = None
        # if obj.get('birthDate'):
        #     birth_date = datetime.strptime(obj.get('birthDate'), "%Y-%m-%d").date()
        # if obj.get('deceasedDateTime'):
        #     deceased_date_time = datetime.strptime(obj.get('deceasedDateTime'), "%Y-%m-%dT%H:%M:%S%z")
        # return Identifier(
        #     id=obj.get('id'),
        #     meta=obj.get('meta'),
        #     text=obj.get('text'),
        #     extension=obj.get('extension'),
        #     active=obj.get('active'),
        #     gender=Gender(obj.get('gender')),
        #     birth_date=birth_date,
        #     deceased_date_time=deceased_date_time,
        #     address=obj.get('address'),
        #     marital_status=obj.get('martialStatus'),
        #     communication=obj.get('communication')
        # )

@dataclass
class Identifier:
    use: IdentifierUse = None
    system: str = None
    value: str = None
    type: dict = None
    # def __init__(self, use=None, age=None, value=None, type=None):
    #     self.use = use
    #     self.system = age
    #     self.value = value
    #     self.type = type


class IdentifierList(db.TypeDecorator):
    impl = db.String

    def process_bind_param(self, value, dialect):
        if value is not None:
            # Serialize the list of Identifier instances to a JSON string
            return json.dumps([vars(identifier) for identifier in value])
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            # Deserialize the JSON string back to a list of Identifier instances
            identifiers_data = json.loads(value)
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
