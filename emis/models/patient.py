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
    resourceType = db.Column(db.String(64))
    meta = db.Column(db.JSON)
    text = db.Column(db.JSON)
    # identifier = db.Column(db.JSON)
    identifiers = db.relationship('Identifier', backref='patient', lazy=True)
    extension = db.Column(db.JSON)
    name = db.relationship('HumanName', backref='patient', lazy=True)
    active = db.Column(db.Boolean, default=True)
    telecom = db.relationship('ContactPoint', backref='patient', lazy=True)
    gender = db.Column(Enum(Gender))
    birthDate = db.Column(db.Date)
    deceasedDateTime = db.Column(db.DateTime)
    address = db.Column(db.JSON)
    maritalStatus = db.Column(db.JSON)
    multipleBirthBoolean = db.Column(db.Boolean)
    communication = db.Column(db.JSON)
