from flask import Flask
from .patient import patient_blueprint


def register_routes(app: Flask) -> None:
    app.register_blueprint(patient_blueprint)
