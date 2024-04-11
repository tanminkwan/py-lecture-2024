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

api.add_resource(FileUpload, '/file')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)