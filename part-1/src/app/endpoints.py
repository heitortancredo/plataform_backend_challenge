from flask import request
from flask import jsonify
from flask_restful import Resource
from datetime import datetime
from app import redisClient
import json

cache = {}

class Products(Resource):

    def post(self):
        data_json = request.get_json()
        dump = json.dumps(data_json, sort_keys=True, indent=2)
        # cached = cache.get(dump)
        cached = redisClient.hget('cache', dump)
        now = datetime.utcnow()

        if cached:
            cached = datetime.strptime(cached, "%Y-%m-%d %H:%M:%S")
            diff =  (now - cached).seconds/60

            if diff < 1:
                return jsonify("rate limiter")

        # cache[dump] = now.strftime("%Y-%m-%d %H:%M:%S")

        redisClient.hset('cache', dump, now.strftime("%Y-%m-%d %H:%M:%S"))

        # return jsonify(cache)
        return jsonify(redisClient.hgetall('cache'))


    def get(self):
        return jsonify(redisClient.hgetall('cache'))
        # return jsonify(cache)
