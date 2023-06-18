from __future__ import annotations
from datetime import datetime
import enum
from typing import Any
from sqlalchemy import Enum
from emis.models.contact_point import ContactPointList
from emis.models.human_name import HumanNameList
from emis.utils.database import db
from emis.utils.utils import JSONSerializableMixin, return_as_dict
from .identifiers import IdentifierList


class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    UNKNOWN = 'unkown'


class Patient(db.Model, JSONSerializableMixin):
    id = db.Column(db.String(64), primary_key=True)
    meta = db.Column(db.JSON)
    name = db.Column(HumanNameList)
    extension = db.Column(db.JSON)
    active = db.Column(db.Boolean)
    gender = db.Column(Enum(Gender))
    birth_date = db.Column(db.Date)
    deceased_date_time = db.Column(db.DateTime)
    address = db.Column(db.JSON)
    marital_status_text = db.Column(db.String(64))
    marital_status_coding = db.Column(db.JSON)
    multiple_birth_boolean = db.Column(db.Boolean)
    communication = db.Column(db.JSON)
    identifier = db.Column(IdentifierList)
    period_start = db.Column(db.DateTime)
    period_end = db.Column(db.DateTime)
    text = db.Column(db.JSON)
    telecom = db.Column(ContactPointList)

    @classmethod
    def prepare_model(cls, obj: dict) -> Patient:

        birth_date = None
        deceased_date_time = None
        if obj.get('birthDate'):
            birth_date = datetime.strptime(obj.get('birthDate'), "%Y-%m-%d").date()
        if obj.get('deceasedDateTime'):
            deceased_date_time = datetime.strptime(obj.get('deceasedDateTime'), "%Y-%m-%dT%H:%M:%S%z")

        identifier_list = []
        if obj.get('identifier'):
            identifier_list = IdentifierList.prepare_type(obj.get('identifier'))

        contact_list = []
        if obj.get('telecom'):
            contact_list = ContactPointList.prepare_type(obj.get('telecom'))

        period_start = None
        period_end = None
        if obj.get('period', {}).get('start'):
            period_start = datetime.strptime(obj.get('period', {}).get('start'), "%Y-%m-%dT%H:%M:%S%z")
        if obj.get('period', {}).get('end'):
            period_end = datetime.strptime(obj.get('period', {}).get('end'), "%Y-%m-%dT%H:%M:%S%z")

        marital_status_text = obj.get('maritalStatus', {}).get('text')
        marital_status_coding = obj.get('maritalStatus', {}).get('coding')
        return Patient(
            id=obj.get('id'),
            meta=obj.get('meta'),
            text=obj.get('text'),
            extension=obj.get('extension'),
            active=obj.get('active'),
            gender=Gender(obj.get('gender')),
            birth_date=birth_date,
            deceased_date_time=deceased_date_time,
            address=obj.get('address'),
            marital_status_text=marital_status_text,
            marital_status_coding=marital_status_coding,
            communication=obj.get('communication'),
            period_start=period_start,
            period_end=period_end,
            identifier=identifier_list,
            telecom=contact_list
        )

    def convert_to_json(self) -> dict[str, Any]:
        return return_as_dict(self)
