import enum
from sqlalchemy import Enum
from emis.utils.database import db


class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    UNKNOWN = 'unkown'


# TODO: period, codeableConcept, coding
class Patient(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    meta = db.Column(db.JSON)
    text = db.Column(db.JSON)
    # identifier = db.Column(db.JSON)
    identifiers = db.relationship('Identifier', backref='patient', lazy=True)
    extension = db.Column(db.JSON)
    name = db.relationship('HumanName', backref='patient', lazy=True)
    active = db.Column(db.Boolean, default=True)
    telecom = db.relationship('ContactPoint', backref='patient', lazy=True)
    gender = db.Column(Enum(Gender))
    birth_date = db.Column(db.Date)
    deceased_date_time = db.Column(db.DateTime)
    address = db.Column(db.JSON)
    marital_status = db.Column(db.JSON)
    multiple_birth_boolean = db.Column(db.Boolean)
    communication = db.Column(db.JSON)
