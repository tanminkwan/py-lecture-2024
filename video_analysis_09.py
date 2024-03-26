"""
prompt:
===
* video.html 의 각 row 맨앞에 "상세보기" 버튼을 추가한다.
* 버튼을 누르면 REST GET /api/v1/detail/<video.id> 가 호출된다.
- 받을 정보는 해당 row 밑에 작은 글씨로 table 구조로 보여준다.
- start, duration, min_similarity 값은 소수 둘째자리에서 반올림한다.

* GET /api/v1/detail/<video.id> 은 video.id에 해당하는 video_split table의 정보를 조회한다.
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
    return render_template('videos_09.html')

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

class AnalyzeVideo(Resource):

    def post(self):
        data = request.get_json()
        video_id = data.get('id')
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
                min_similarity=group['min_similarity'],
                min_frame_path=group['min_frame_path'],
                max_frame_path=group['max_frame_path']
            )
            db.session.add(video_split)

        db.session.commit()

        return {'message': 'Video analysis completed and saved for video ID: {}'.format(video_id)}

class VideoDetails(Resource):
    def get(self, video_id):
        video_details = VideoSplit.query.filter_by(video_id=video_id).all()
        video_details_list = []
        for detail in video_details:

            start_rounded = round(detail.start, 2)  # 소수 둘째 자리에서 반올림
            duration_rounded = round(detail.duration, 2)  # 소수 둘째 자리에서 반올림
            min_similarity_rounded = round(detail.min_similarity, 2)  # 소수 둘째 자리에서 반올림

            video_details_list.append({
                'group_number': detail.group_number,
                'min_frame_number': detail.min_frame_number,
                'max_frame_number': detail.max_frame_number,
                'frame_count': detail.frame_count,
                'start': start_rounded,
                'duration': duration_rounded,
                'min_similarity': min_similarity_rounded,
                'min_frame_path': detail.min_frame_path,
                'max_frame_path': detail.max_frame_path
            })
        
        return video_details_list
                
api.add_resource(FileUpload, '/upload')
api.add_resource(VideoList, '/videos')
api.add_resource(AnalyzeVideo, '/analyze')
api.add_resource(VideoDetails, '/detail/<int:video_id>')
                 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)