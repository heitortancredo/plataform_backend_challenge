from flask import Flask
from flask_restful import Api
from flask import Blueprint
import redis

redisClient = redis.StrictRedis(host='localhost',
                                port=6379,
                                db=0,
                                charset="utf-8",
                                decode_responses=True)

def create_app(config='config.cfg'):
    from app.endpoints import Products

    app = Flask(__name__)
    app.config.from_pyfile(config)
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    api.add_resource(Products, '/v1/products')
    app.register_blueprint(api_bp)

    return app
