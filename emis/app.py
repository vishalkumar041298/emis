import os
from dotenv import load_dotenv
from flask import Flask
from emis.routes import register_routes
from emis.utils.database import db


load_dotenv()


app = Flask(__name__)

host = os.environ.get('HOST')
port = os.environ.get('PORT')
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
database_name = os.environ.get('DATABASE_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
register_routes(app)

if __name__ == '__main__':
    app.run()
