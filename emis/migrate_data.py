import argparse
from collections import defaultdict
import json
from typing import Any
from emis.models.encounter import Encounter
from emis.models.observation import Observation
from emis.models.patient import Patient
from .app import app, db
from .util_functions import fetch_json_files


resource_type_method_mapper = {
    "Patient":  Patient,
    "Encounter": Encounter,
    "Observation": Observation,
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-P', '--data-path', required=False, default='data')
    args = parser.parse_args()
    path = args.data_path
    files = fetch_json_files(path)
    all_models = defaultdict(list)
    model_class: Any
    with app.app_context():
        db.create_all()
        for file in files:
            print("file: ", file)
            with open(file, 'r', encoding='utf-8') as f:
                obj = json.load(f)
            patient_id = None
            for entry in obj['entry']:
                resource = entry['resource']
                resource_type = entry['resource']['resourceType']
                if resource_type in resource_type_method_mapper:
                    model_class = resource_type_method_mapper[resource_type]
                    model_obj = model_class.prepare_model(resource)
                    all_models[resource_type].append(model_obj)

        for resource_type, _ in resource_type_method_mapper.items():
            print(resource_type)
            models = all_models.get(resource_type)
            if models:
                db.session.bulk_save_objects(models)
        db.session.commit()
