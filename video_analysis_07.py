"""
prompt:
===
GET /api/v1/videos 에 video.id 값을 추가한다.
videos.html 의 각 row의 맨 앞에 video.id 값을 보여준다.
videos.html 의 각 row의 끝에 '분석 실행' 이라는 버튼을 추가한다

REST POST /api/v1/analyze 를 추가한다.
이 버튼을 click 하면 POST /api/v1/analyze 를 호출한다.
	- data 는 Video.id 하나이며 header가 아닌 body에 담는다.
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
    return render_template('videos_07.html')

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

class VideoList(Resource):

    def get(self):
        videos = Video.query.all()
        video_list = []
        for video in videos:
            video_list.append({
                'id': video.id,
                'file_name': video.file_name,
                'file_extension': video.file_extension,
                'file_size': video.file_size,
                'created_at': video.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        return video_list

class AnalyzeVideo(Resource):

    def post(self):
        data = request.get_json()
        video_id = data.get('id')
        # 여기에 비디오 분석 로직 추가
        # video_id를 사용하여 특정 비디오 분석
        # 예를 들어, 비디오 ID에 해당하는 파일을 찾아 분석을 시작할 수 있습니다.
        # 이 예시에서는 단순히 ID를 받아서 성공적으로 분석 시작되었다고 가정하고 메시지만 반환합니다.
        return {'message': f'Video analysis started for video ID: {video_id}'}
            
api.add_resource(HomeAPI, '/home')
api.add_resource(FileUpload, '/upload')
api.add_resource(VideoList, '/videos')
api.add_resource(AnalyzeVideo, '/analyze')
                 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)