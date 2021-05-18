from flask_restful import Resource
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func


class Health(Resource):
    def get(self):
        return {"message": "Feature 1 Flask App is working, please use postman"}
