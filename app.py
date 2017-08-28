from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json
import requests

app = Flask(__name__)

app.config.from_pyfile('config.py')

pg_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# create a configured "Session" class
Session = sessionmaker(bind=pg_engine)

# create a Session
session = Session()


db = SQLAlchemy(app)

from views import *

if __name__ == '__main__':
    app.run(port=5555)
