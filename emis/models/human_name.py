import enum
from sqlalchemy import Enum
from sqlalchemy.orm import validates
from emis.utils.database import db


class HumanNameUse(enum.Enum):
    USUAL = 'usual'
    OFFICIAL = 'official'
    TEMP = 'temp'
    NICKNAME = 'nickname'
    ANONYMOUS = 'anonymous'
    OLD = 'old'
    MAIDEN = 'maiden'


class HumanName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    use = db.Column(Enum(HumanNameUse))
    text = db.Column(db.String(64))
    family_name = db.Column(db.String(64))
    given = db.Column(db.JSON)
    prefix = db.Column(db.JSON)
    suffix = db.Column(db.JSON)
    patient_id = db.Column(db.String(64), db.ForeignKey('patient.id'))

    @validates('rank')
    def validate_positive_integer(self, key: str, value: int) -> int:
        if value and value <= 0:
            raise ValueError('Rank should not be less than 0')
        return value

