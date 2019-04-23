from flask import request
from flask import jsonify
from flask_restful import Resource
from datetime import datetime
import json

cache = {}

class Products(Resource):

    def post(self):
        data_json = request.get_json()
        dump = json.dumps(data_json, sort_keys=True, indent=2)
        cached = cache.get(dump)

        if cached:
            now = datetime.utcnow()
            diff =  (now - cached).seconds/60

            if diff < 1:
                return jsonify("rate limiter")

        cache[dump] = datetime.utcnow()

        return jsonify(cache)


    def get(self):
        return jsonify(cache)
