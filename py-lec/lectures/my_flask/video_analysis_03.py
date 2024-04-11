from flask import Flask
from flask_restful import Api, Resource


app = Flask(import_name=__name__)

api = Api(app, prefix="/api/v1")

# REST API
class HomeAPI(Resource):

    def get(self, username):
        message = f'{username}님 환영합니다.'
        return {'result': message}, 200

api.add_resource(HomeAPI, '/home/<string:username>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)