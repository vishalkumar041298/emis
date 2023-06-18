import argparse
from collections import defaultdict
import json
from app import app, db
from emis.models.encounter import Encounter
from emis.models.identifiers import Identifier
from emis.models.observation import Observation
from emis.models.patient import Patient
from util_functions import fetch_json_files


resource_type_method_mapper = {
    "Patient":  Patient,
    "Observation": Observation,
    "Encounter": Encounter,
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-P', '--data-path', required=False, default='data')
    args = parser.parse_args()
    path = args.data_path
    files = fetch_json_files(path)
    all_models = defaultdict(list)
    with app.app_context():
        db.create_all()
        for file in files:
            with open(file) as f:
                obj = json.load(f)
            type = obj['type']
            patient_id = None
            for entry in obj['entry']:
                resource = entry['resource']
                resource_type = entry['resource']['resourceType']
                if resource_type in resource_type_method_mapper:
                    if resource_type == 'Patient':
                        patient_id = resource['id']
                        model_class = resource_type_method_mapper[resource_type]
                        model_obj = model_class.prepare_model(resource)
                        all_models[resource_type].append(model_obj)
