"""
prompt:
===
video table 정보를 모두 읽어서 html로 조회하는 code를 추가하라

조건 : 
- html은 videos.html 파일이다.
- html에 접근하는 url은 /videos 이다
- video table 정보를 조회하는 REST API의 경로는 /api/v1/videos 이다.
- videos.html에서 GET /api/v1/videos 을 호출한다.
- videos.html 은 table 구조로 예쁘게 만들어라
- file upload가 완료되면 /videos 로 redirect 되도록 해라.upload.html 만 수정하라.
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
    return render_template('upload_06.html')

@app.route("/videos")
def video_list():
    return render_template('videos_06.html')

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

class VideoList(Resource):

    def get(self):
        videos = Video.query.all()
        video_list = []
        for video in videos:
            video_list.append({
                'file_name': video.file_name,
                'file_extension': video.file_extension,
                'file_size': video.file_size,
                'created_at': video.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        return video_list
        
api.add_resource(FileUpload, '/upload')
api.add_resource(VideoList, '/videos')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)