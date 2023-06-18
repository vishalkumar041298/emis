import os
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv
from flask import Flask
from emis.models import *
from emis.routes import register_routes
from emis.utils.database import db


app = Flask(__name__)

# Loading Credentials
load_dotenv()
host = os.environ.get('HOST')
port = os.environ.get('PORT')
username = os.environ.get('DB_USERNAME')
password = os.environ.get('PASSWORD')
database_name = os.environ.get('DATABASE_NAME')

database_uri = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database_name}'

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating Database if not exists
engine = create_engine(database_uri)
if not database_exists(engine.url):
    create_database(engine.url)

db.init_app(app)
register_routes(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
