from flask import Blueprint, jsonify, request, Response
from emis.models.patient import Patient
from emis.utils.database import db

patient_blueprint = Blueprint('patient', __name__)


@patient_blueprint.route('/patient', methods=['GET'])
def get_patient() -> Response:
    patient_records = Patient.query.all()
    records = []
    for record in patient_records:
        rec = record.convert_to_json()
        if '_sa_instance_state' in rec:
            del rec['_sa_instance_state']
        records.append(rec)
    return jsonify({"data": records})


@patient_blueprint.route('/patient/<int:page>', methods=['GET'])
def get_patient_paginated(page: int = 1) -> Response:
    patients = Patient.query.paginate(page=page, per_page=20)
    patient_records = patients.items
    records = []
    for record in patient_records:
        rec = record.convert_to_json()
        if '_sa_instance_state' in rec:
            del rec['_sa_instance_state']
        records.append(rec)
    return jsonify({"data": records})


@patient_blueprint.route('/patient', methods=['POST'])
def create_patient() -> Response:
    # Create a new patient record
    data = request.get_json()
    field = data.get('field')
    new_patient = Patient(field=field)
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'patient record created successfully'})
