from flask import request
from flask import jsonify
from flask import Response
from flask_restful import Resource
from datetime import datetime
from app import redisClient
import json
import xxhash

# cache = {}

class Products(Resource):

    def post(self):
        data_json = request.get_json()

        # dump to string to use as hash key
        dump = json.dumps(data_json, sort_keys=True)

        """
        Uses hash-algorithm because very long keys are not a good idea and the
        maximum allowed key size in Redis is 512 MB.
        xxHash is an extremely fast non-cryptographic hash algorithm, working
        at speeds close to RAM limits. Link: https://cyan4973.github.io/xxHash/
        """
        dump =  xxhash.xxh64_hexdigest(dump, seed=102938)

        # cached = cache.get(dump)

        # creates one hash for every request because redis only have "expires
        # feature" for entire hash not for yours items... =(
        cached = redisClient.hget(dump, dump)
        now = datetime.utcnow()

        if cached:
            # Datetime to string - Redis not suport datetime objects
            cached = datetime.strptime(cached, "%Y-%m-%d %H:%M:%S")
            diff =  (now - cached).seconds/60

            if diff < 10: # 10 minutes
            # if diff < 1:
                return Response("Forbidden", status=403)


        # cache[dump] = now.strftime("%Y-%m-%d %H:%M:%S")

        redisClient.hset(dump, dump, now.strftime("%Y-%m-%d %H:%M:%S"))
        redisClient.expire(dump, 660)  # TTL = 11 min

        # return jsonify(cache)
        return jsonify(redisClient.hgetall(dump))
