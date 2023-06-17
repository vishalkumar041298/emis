import enum
from sqlalchemy import Enum
from emis.utils.database import db


class EncounterStatus(enum.Enum):
    PLANNED = 'planned'
    IN_PROGRESS = 'in-progress'
    ON_HOLD = 'on-hold'
    DISCHARGED = 'discharged'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    DISCONTINUED = 'discontinued'
    ENTERED_IN_ERROR = 'entered-in-error'
    UNKNOWN = 'unknown'


class Encounter(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    meta = db.Column(db.JSON)
    status = db.Column(Enum(EncounterStatus))
    identifier = db.relationship('Identifier', backref='encounter', lazy=True)
    meta = db.Column(db.JSON)
    service_provider = db.Column(db.String(64))
    reason_code = db.Column(db.JSON)
    subject = db.Column(db.JSON)
    location = db.Column(db.String(64))
    participant = db.Column(db.JSON)
    enounter_class = db.Column(db.JSON)
    patient_id = db.Column(db.String(64), db.ForeignKey('patient.id'))
