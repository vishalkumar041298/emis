import enum
from sqlalchemy import Enum
from sqlalchemy.orm import validates
from emis.utils.database import db
from emis.utils.utils import JSONSerializableMixin


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


class ContactPoint(db.Model, JSONSerializableMixin):
    id = db.Column(db.Integer, primary_key=True)
    system = db.Column(Enum(ContactPointSystem))
    value = db.Column(db.String(128))
    use = db.Column(Enum(ContactPointUse))
    rank = db.Column(db.Integer)
    patient_id = db.Column(db.String(64), db.ForeignKey('patient.id'))

    @validates('rank')
    def validate_positive_integer(self, key: str, value: int) -> int:
        if value and value <= 0:
            raise ValueError('Rank should not be less than 0')
        return value
