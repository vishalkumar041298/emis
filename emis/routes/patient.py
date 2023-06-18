from flask import Blueprint, jsonify, request, Response
from emis.models.patient import Patient
from emis.utils.database import db

patient_blueprint = Blueprint('patient', __name__)


@patient_blueprint.route('/patient', methods=['GET'])
def get_patient() -> Response:
    patient_records = Patient.query.all()
    response = [{'id': record.id, 'field': record.field} for record in patient_records]
    return jsonify(response)


@patient_blueprint.route('/patient', methods=['POST'])
def create_patient() -> Response:
    # Create a new patient record
    data = request.get_json()
    field = data.get('field')
    new_patient = Patient(field=field)
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'patient record created successfully'})
