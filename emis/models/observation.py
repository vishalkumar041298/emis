import enum
from sqlalchemy import Enum
from emis.utils.database import db
from emis.utils.utils import remove_urn


class ObservationStatus(enum.Enum):
    REGISTERED = 'registered'
    PRELIMINARY = 'preliminary'
    FINAL = 'final'
    AMENDED = 'amended'
    CORRECTED = 'corrected'
    CANCELLED = 'cancelled'
    ENTERED_IN_ERROR = 'entered-in-error'
    UNKNOWN = 'unknown'


class Observation(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    meta = db.Column(db.JSON)
    identifier = db.relationship('Identifier', backref='observation', lazy=True)
    status = db.Column(Enum(ObservationStatus))
    category = db.Column(db.JSON)
    issued = db.Column(db.DateTime)
    value_codeable_concept = db.Column(db.JSON)
    value_quantity = db.Column(db.JSON)
    subject = db.Column(db.JSON)
    effective_date_time = db.Column(db.DateTime)
    code = db.Column(db.JSON)
    component = db.Column(db.JSON)
    patient_id = db.Column(db.String(64), db.ForeignKey('patient.id'))
    enounter_id = db.Column(db.String(64), db.ForeignKey('patient.id'))

    def save(self, *args, **kwargs):
        preprocessed_value = remove_urn(self.enounter_id)
        self.enounter_id = preprocessed_value
        super().save(*args, **kwargs)
