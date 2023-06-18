from __future__ import annotations
from datetime import datetime
import enum
from sqlalchemy import Enum
from emis.utils.database import db
from emis.utils.utils import JSONSerializableMixin
from .identifiers import IdentifierList


class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    UNKNOWN = 'unkown'


# TODO: period, codeableConcept, coding
class Patient(db.Model, JSONSerializableMixin):
    id = db.Column(db.String(64), primary_key=True)
    meta = db.Column(db.JSON)
    text = db.Column(db.JSON)
    name = db.relationship('HumanName', backref='patient', lazy=True)
    # identifier = db.Column(db.JSON)
    extension = db.Column(db.JSON)
    active = db.Column(db.Boolean)
    gender = db.Column(Enum(Gender))
    birth_date = db.Column(db.Date)
    deceased_date_time = db.Column(db.DateTime)
    address = db.Column(db.JSON)
    marital_status = db.Column(db.JSON)
    multiple_birth_boolean = db.Column(db.Boolean)
    communication = db.Column(db.JSON)
    identifiers = db.Column(IdentifierList)
    telecom = db.relationship('ContactPoint', backref='patient', lazy=True)

    @classmethod
    def prepare_model(cls, obj: dict) -> Patient:
        birth_date = None
        deceased_date_time = None
        identifier_list = None
        if obj.get('birthDate'):
            birth_date = datetime.strptime(obj.get('birthDate'), "%Y-%m-%d").date()
        if obj.get('deceasedDateTime'):
            deceased_date_time = datetime.strptime(obj.get('deceasedDateTime'), "%Y-%m-%dT%H:%M:%S%z")
        if obj.get('identifier'):
            identifier_list = IdentifierList.prepare_type(obj.get('identifier'))

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
            marital_status=obj.get('martialStatus'),
            communication=obj.get('communication'),
            identifier_list=identifier_list
        )
