"""
prompt:
===
1. from functions import analyze_video 를 추가한다.
- analyze_video 를 호출했을 때 return 값의 sample은 아래와 같다.
simularity_groups = \
[
    {
        'group_number': 0, 
        'min_frame_number': 1, 
        'max_frame_number': 30, 
        'frame_count': 30, 
        'start': 0.05, 
        'duration': 1.5, 
        'dynamic_intensity': 0.0011207513559413,
        'min_similarity': 0.9771207513559413, 
        'min_frame_path': 'tmp/capture_1.png', 
        'max_frame_path': 'tmp/capture_30.png'
        }, 
    {
        'group_number': 1, 
        'min_frame_number': 31, 
        'max_frame_number': 183, 
        'frame_count': 153, 
        'start': 1.55, 
        'duration': 7.65, 
        'dynamic_intensity': 0.1271207513559413,
        'min_similarity': 0.8046356748819421, 
        'min_frame_path': 'tmp/capture_31.png', 
        'max_frame_path': 'tmp/capture_183.png'}
]

2. flask_sqlalchemy.SQLAlchemy.Model 을 사용하여 Table을 정의
- Table 이름은 video_split
- column들은 위의 simularity_groups 의 항목들과 일치
- Video class의 id를 foreign key로 가짐

3. VideoDetails.post 함수에 아래 조건을 만족하는 code 추가하라

조건:
- video_id 로 video table에서 file_name 을 읽는다
- simularity_groups값을 아래와 같이 얻는다.
  file_path = UPLOAD_FOLDER + '/' + file_name
  simularity_groups = analyze_video(file_path)
- simularity_groups 정보를 database table에 insert 한다.
===
응답 모델 : ChatGPT-3.5
"""
import os
from flask import Flask, render_template, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from functions import analyze_video

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

class VideoSplit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    group_number = db.Column(db.Integer, nullable=False)
    min_frame_number = db.Column(db.Integer)
    max_frame_number = db.Column(db.Integer)
    frame_count = db.Column(db.Integer)
    start = db.Column(db.Float)
    duration = db.Column(db.Float)
    dynamic_intensity = db.Column(db.Float)
    min_similarity = db.Column(db.Float)
    min_frame_path = db.Column(db.String(255))
    max_frame_path = db.Column(db.String(255))

    def __repr__(self):
        return f"<VideoSplit {self.id}>"

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

class VideoDetails(Resource):

    def post(self, video_id):
        # 여기에 비디오 분석 로직 추가
        # video_id로 video table에서 file_name을 읽음
        video = Video.query.get(video_id)
        if video is None:
            return {'error': 'Video not found'}, 404

        # file_path로 비디오 분석
        file_path = os.path.join(UPLOAD_FOLDER, video.file_name)
        simularity_groups = analyze_video(file_path)

        # 비디오 분석 결과를 VideoSplit 테이블에 저장
        for group in simularity_groups:
            video_split = VideoSplit(
                video_id=video_id,
                group_number=group['group_number'],
                min_frame_number=int(group['min_frame_number']),
                max_frame_number=int(group['max_frame_number']),
                frame_count=int(group['frame_count']),
                start=group['start'],
                duration=group['duration'],
                dynamic_intensity=group['dynamic_intensity'],
                min_similarity=group['min_similarity'],
                min_frame_path=group['min_frame_path'],
                max_frame_path=group['max_frame_path']
            )
            db.session.add(video_split)

        db.session.commit()

        return {'message': f'Video analysis completed and saved for video ID: {video_id}'}

api.add_resource(FileUpload, '/file')
api.add_resource(VideoList, '/videos')
api.add_resource(VideoDetails, '/video_details/<int:video_id>')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)