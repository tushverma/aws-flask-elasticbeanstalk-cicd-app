from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.item import ItemModel
from flask_jwt_extended.utils import create_access_token, get_jwt, get_jwt_identity
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

# from sqlalchemy.ext.declarative import api


class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.query.all()]
        if user_id:
            return {"items": items}

        return {"items": [], "message": "Please login first"}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank')
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='This field cannot be left blank')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404
    @jwt_required(fresh=True)
    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {f"message": f"An item with name {name} already exists."}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        item_json = item.json()
        try:
            item.save_to_db()
            return item_json, 201
        except Exception as e:
            print(e)
            return {"message": f"an error occured."}, 500

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'You need to be an admin'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item Deleted"}
        return {'message': 'No Item for this name'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()
