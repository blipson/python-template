from datetime import datetime
from flask import Flask, request, Response, jsonify
from flask.ext.cors import CORS
from flask_swagger import swagger
from logging.handlers import RotatingFileHandler
import config
import db
import json
import logging

# app setup and config
app = Flask(__name__)
CORS(app)
PERSIST_HISTORY = config.CONF['app']['persist_history']
ID_HEADER = 'X-Authorization-Token'
app.config['DEBUG'] = config.CONF['app']['debug']

def alchemyencoder(obj):
    if id(type) and type(obj) in (datetime, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/profile/<string:env>', methods=['GET'])
def export_company_details(env):
    app.logger.info('Getting profile info')
    res = db.run_query(env, 'SELECT * FROM DC4CONFIG.PROFILE')
    return Response(json.dumps([dict(r) for r in res],
                      default=alchemyencoder), mimetype='application/json', status=200)

if __name__ == '__main__':
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=config.CONF['app']['port'])