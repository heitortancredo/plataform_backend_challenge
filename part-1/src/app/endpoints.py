from flask import request
from flask import current_app
from flask import Response
from flask_restful import Resource
from app import redisClient
import json
import xxhash

# cache = {}
hash_seed = 102938

class Products(Resource):

    def post(self):
        data_json = request.get_json()

        status = self.rate_limiter(data_json)

        if not status:
            return Response("Forbidden", status=403)

        return Response('OK', status=200)

    def rate_limiter(self, data):
        # dump to string to use as hash key
        dump = json.dumps(data, sort_keys=True)

        """
        Uses hash-algorithm because very long keys are not a good idea and the
        maximum allowed key size in Redis is 512 MB.
        xxHash is an extremely fast non-cryptographic hash algorithm, working
        at speeds close to RAM limits. Link: https://cyan4973.github.io/xxHash/
        """
        dump_hash =  xxhash.xxh64_hexdigest(dump, seed=hash_seed)

        cached = redisClient.get(dump_hash)

        if cached:
            return False

        app = current_app

        if not app.testing:
            redisClient.setex(dump_hash, 10*60, dump_hash)  # TTL = 10 min
        else:
            redisClient.setex(dump_hash, 1, dump_hash)  # TTL = 2 secs

        return  True
