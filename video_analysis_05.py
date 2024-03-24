"""
prompt:
===
flask-sqlalchemy를 사용하여
upload 된 파일 정보를 database에 저장하는 code를 추가하라

조건:
- flask_sqlalchemy.SQLAlchemy.Model 을 사용하여 Table을 정의
- database 접속 정보 : sqlite:///mydb.db
- model class 이름 : Video
- table 이름 : video
- column 정보 :
	file 이름
	file 확장자 이름
	file size
	등록시간
===
응답 모델 : ChatGPT-3.5
"""
import os
from flask import Flask, render_template, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = 'upload'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(import_name=__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videodb.db'

api = Api(app, prefix="/api/v1")

db = SQLAlchemy(app)

# 모델 정의
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_extension = db.Column(db.String(10), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Video {self.id}>"

# 아래 line은 LLM이 잘못 알려줘 수정함
# LLM : 
#db.create_all()
# 변경 : 
with app.app_context():
    db.create_all()

@app.route("/upload")
def upload():
    return render_template('upload.html')

# REST API
class HomeAPI(Resource):

    def get(self):
        message = "동영상을 분석해 드립니다."
        return {'result': message}, 200

class FileUpload(Resource):
    
    def post(self):
        if 'file' not in request.files:
            return {'message': 'No file part'}, 400

        file = request.files['file']
        if file.filename == '':
            return {'message': 'No selected file'}, 400

        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)

        # 파일 정보를 데이터베이스에 저장
        video = Video(
            file_name=file.filename,
            file_extension=os.path.splitext(file.filename)[1],
            file_size=os.path.getsize(filename),
            created_at=db.func.now()
        )
        db.session.add(video)
        db.session.commit()

        return {'message': 'File uploaded successfully', 'filename': filename}, 201
    
api.add_resource(HomeAPI, '/home', endpoint='home')
api.add_resource(FileUpload, '/upload')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)