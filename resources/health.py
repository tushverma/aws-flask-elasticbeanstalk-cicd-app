from flask_restful import Resource
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func


class Health(Resource):
    def get(self):
        return {"message": "App is working"}
