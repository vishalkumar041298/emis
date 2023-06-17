import enum
from emis.utils.database import db
from sqlalchemy import Enum


class IdentifierUse(enum.Enum):
    USUAL = 'usual'
    OFFICIAL = 'official'
    TEMP = 'temp'
    SECONDARY = 'secondary'
    OLD = 'old'


class Identifier(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    use = db.Column(Enum(IdentifierUse))
    type = db.Column(db.JSON)
    system = db.Column(db.String(128))
    value = db.Column(db.String(128))
    patient_id = db.Column(db.String(64), db.ForeignKey('patient.id'))
