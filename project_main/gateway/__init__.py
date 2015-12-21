from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
 
logging.basicConfig(filename='gateway.log',level=logging.INFO,format='%(asctime)s --- %(message)s')