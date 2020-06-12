from index import Inverted
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import json

index = Inverted('twitter_tracking/clean')

app = Flask(__name__)
CORS(app)

@app.route('/')
def query():
    return jsonify(index.query(request.args.get('q'), request.args.get('limit')))
