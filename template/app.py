from flask import Flask, request, Response, jsonify
from flask.ext.cors import CORS
from flask_swagger import swagger

# app setup and config
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'