from __future__ import annotations
from datetime import datetime
import enum
from typing import Any
from sqlalchemy import Enum
from emis.models.identifiers import IdentifierList
from emis.utils.database import db
from emis.utils.utils import remove_urn, return_as_dict


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
    identifier = db.Column(IdentifierList)
    status = db.Column(Enum(ObservationStatus))
    category = db.Column(db.JSON)
    issued = db.Column(db.DateTime)
    value_codeable_concept = db.Column(db.JSON)
    value_quantity_value = db.Column(db.Float)
    value_quantity_unit = db.Column(db.String(20))
    value_quantity_system = db.Column(db.String(128))
    value_quantity_code = db.Column(db.String(64))
    effective_date_time = db.Column(db.DateTime)
    code = db.Column(db.JSON)
    component = db.Column(db.JSON)
    patient_id = db.Column(db.String(64), db.ForeignKey('patient.id'), nullable=True)
    encounter_id = db.Column(db.String(64), db.ForeignKey('encounter.id'), nullable=True)

    @classmethod
    def prepare_model(cls, obj: dict) -> Observation:

        identifier_list = []
        if obj.get('identifier'):
            identifier_list = IdentifierList.prepare_type(obj.get('identifier'))

        issued = None
        if obj.get('issued'):
            issued = datetime.strptime(obj.get('issued'), "%Y-%m-%dT%H:%M:%S.%f%z")
            # try:
            #     issued = datetime.strptime(obj.get('issued'), "%Y-%m-%dT%H:%M:%S%z")
            # except Exception as e:
            #     print("Exception: ", str(e))

        effective_date_time = None
        if obj.get('effectiveDateTime'):
            effective_date_time = datetime.strptime(obj.get('effectiveDateTime'), "%Y-%m-%dT%H:%M:%S%z")

        v_code = None
        v_value = None
        v_unit = None
        v_system = None
        if obj.get('valueQuantity'):
            vq = obj.get('valueQuantity')
            v_code = vq.get('code')
            v_value = vq.get('value')
            v_unit = vq.get('unit')
            v_system = vq.get('system')

        patient_id = None
        if obj.get('subject'):
            patient_id = remove_urn(obj.get('subject').get('reference'))

        encounter_id = None
        if obj.get('encounter'):
            encounter_id = remove_urn(obj.get('encounter').get('reference'))

        return Observation(
            id=obj.get('id'),
            meta=obj.get('meta'),
            identifier=identifier_list,
            status=ObservationStatus(obj.get('status')),
            category=obj.get('category'),
            issued=issued,
            value_codeable_concept=obj.get('valueCodeableConcept'),
            value_quantity_value=v_value,
            value_quantity_unit=v_unit,
            value_quantity_system=v_system,
            value_quantity_code=v_code,
            effective_date_time=effective_date_time,
            code=obj.get('code'),
            component=obj.get('component'),
            patient_id=patient_id,
            encounter_id=encounter_id,
        )

    def convert_to_json(self) -> dict[str, Any]:
        return return_as_dict(self)
