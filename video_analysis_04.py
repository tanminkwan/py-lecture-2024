"""
prompt:
===
from flask import Flask
from flask_restful import Api, Resource

app = Flask(import_name=__name__)
api = Api(app, prefix="/api/v1")

위 code를 사용하여를 사용해서
REST API로 file upload python code를 짜라.
file upload 화면 html 도 만들어라.
다음 조건을 만족한다.
---
- upload folder 는 './upload' 이다
- REST API 경로는 /api/v1/upload 이다
===
응답 모델 : ChatGPT-3.5
"""
import os
from flask import Flask, render_template, request
from flask_restful import Api, Resource

UPLOAD_FOLDER = 'upload'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(import_name=__name__)

api = Api(app, prefix="/api/v1")

@app.route("/upload")
def upload():
    return render_template('upload_04.html')

# REST API
class FileUpload(Resource):
    
    def post(self):
        if 'file' not in request.files:
            return {'message': 'No file part'}, 400

        file = request.files['file']
        if file.filename == '':
            return {'message': 'No selected file'}, 400

        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        return {'message': 'File uploaded successfully', 'filename': filename}, 201
    
api.add_resource(FileUpload, '/upload')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)