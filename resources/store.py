import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse
import flask.scaffold
# from sqlalchemy.ext.declarative import api
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "Store not found"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": f"A store with name {name} already exists."}, 400
        store = StoreModel(name)
        store_json = store.json()
        try:
            store.save_to_db()
        except:
            return {"message": "An error occur while creating store."}, 500
        return store_json, 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        try:
            store.delete_from_db()
        except:
            return {"message": "An error occur while creating store."}, 500
        return {"message": "Store deleted"}


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.find_all()]}
