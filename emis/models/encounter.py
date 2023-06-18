from __future__ import annotations
from datetime import datetime
import enum
from typing import Any
from sqlalchemy import Enum
from emis.models.identifiers import IdentifierList
from emis.utils.database import db
from emis.utils.utils import remove_urn, return_as_dict


class EncounterStatus(enum.Enum):
    PLANNED = 'planned'
    IN_PROGRESS = 'in-progress'
    ON_HOLD = 'on-hold'
    DISCHARGED = 'discharged'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    DISCONTINUED = 'discontinued'
    ENTERED_IN_ERROR = 'entered-in-error'
    FINISHED = 'finished'
    UNKNOWN = 'unknown'


class Encounter(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    meta = db.Column(db.JSON)
    status = db.Column(Enum(EncounterStatus))
    identifier = db.Column(IdentifierList)
    meta = db.Column(db.JSON)
    service_provider = db.Column(db.Text)
    reason_code = db.Column(db.JSON)
    location = db.Column(db.JSON)
    participant = db.Column(db.JSON)
    encounter_class = db.Column(db.JSON)
    individual = db.Column(db.String(64))
    period_start = db.Column(db.DateTime)
    period_end = db.Column(db.DateTime)
    patient_id = db.Column(db.String(64), db.ForeignKey('patient.id'))

    @classmethod
    def prepare_model(cls, obj: dict) -> Encounter:
        period_start = None
        period_end = None
        identifier_list = []
        if obj.get('period', {}).get('start'):
            period_start = datetime.strptime(obj.get('period', {}).get('start'), "%Y-%m-%dT%H:%M:%S%z")

        if obj.get('period', {}).get('end'):
            period_end = datetime.strptime(obj.get('period', {}).get('end'), "%Y-%m-%dT%H:%M:%S%z")

        individual = obj.get('individual', {}).get('display')
        if obj.get('identifier'):
            identifier_list = IdentifierList.prepare_type(obj.get('identifier'))

        patient_id = None
        if obj.get('subject'):
            patient_id = remove_urn(obj.get('subject').get('reference'))

        return Encounter(
            id=obj.get('id'),
            meta=obj.get('meta'),
            status=EncounterStatus(obj.get('status')),
            identifier=identifier_list,
            encounter_class=obj.get('class'),
            patient_id=patient_id,
            individual=individual,
            participant=obj.get('partipant'),
            reason_code=obj.get('reasonCode'),
            service_provider=obj.get('serviceProvider', {}).get("display"),
            location=obj.get('location'),
            period_start=period_start,
            period_end=period_end,
        )

    def convert_to_json(self) -> dict[str, Any]:
        return return_as_dict(self)
