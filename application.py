#!/Users/tverma/flask_web_dev/udemy/section6/venv/bin/python
from resources.store import Store, StoreList
from resources.item import Item, ItemList
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.health import Health
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask import Flask
from blacklist import BLACKLIST
from db import db
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['PROPAGATE_EXCEPTIONS'] = True
application.config['JWT_BLACKLIST_ENABLED'] = True
application.config['JWT_BLACKLIST_TOKEN_CHECKS']=['access', 'refresh']
application.secret_key = 'tverma'
api = Api(application)
db.init_app(app=application)

@application.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(application)


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.expired_token_loader
def expired_token_loader():
    return {
        "description":"The token has expired",
        "error":"token_expired",
    }, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {"description":"Signature Verification Failed",
    "error":"invalid loader"}, 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return {"description":"Request Does not have an access token",
        "error":"Token not found"}, 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(header, payload):
    return {"description":"Token is not fresh",
        "error":"fresh_token_required"}, 401

@jwt.revoked_token_loader
def revoked_token_callback(headr, payload):
    return {"description":"Token has been revoked",
        "error":"token_revoked"}, 401

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(header, payload):
    return True if  payload['jti'] in BLACKLIST else False



api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(Health, '/')

if __name__ == '__main__':
    # db.init_app(app=application)
    application.run(port=5000, debug=True)
