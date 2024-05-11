## 실습 방식
my_flask/video_analysis.py에 기능들을 하나씩 추가하고 OS prompt(windows shell)상에서 실행 후 해당 기능을 확인하는 방식으로 실습을 진행합니다.

## STEP 1. mp4 파일 upload 하기
- 사용자가 웹 페이지를 통해 파일을 업로드하고, 서버가 이를 처리하여 지정된 폴더에 저장하는 기능을 구현합니다.
- 참고 파일 : my_flask/video_analysis_09.py
### 1. 추가된 Code
```python
# 추가 : 필요한 모듈 가져오기
import os
from flask import Flask, render_template, request
from flask_restful import Api, Resource

# 추가 : 업로드 폴더 설정
UPLOAD_FOLDER = 'upload'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 추가 : Flask 애플리케이션 및 API 설정
app = Flask(import_name=__name__)

api = Api(app, prefix="/api/v1")

# 추가 : 업로드 페이지 라우트
@app.route("/upload")
def upload():
    return render_template('upload_04.html')

# 추가 : 파일 업로드 API
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

# 추가 : 애플리케이션 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```
### 2. Code 설명
#### **필요한 모듈 가져오기**: 
- 운영 체제와의 상호작용, Flask 애플리케이션 생성, 템플릿 렌더링, 클라이언트 요청 처리, 그리고 REST API 구축을 위한 모듈을 불러옵니다.
#### **업로드 폴더 설정**:
- 업로드된 파일을 저장할 `upload` 폴더를 설정하고, 폴더가 없으면 생성합니다.
#### **Flask 애플리케이션 및 API 설정**:
- Flask 애플리케이션 인스턴스를 생성하고, `/api/v1` 접두어를 가진 API 인스턴스를 설정합니다.
#### **업로드 페이지 라우트**:
- 사용자가 파일을 업로드할 수 있는 웹 페이지로 이동하게 하는 `/upload` 경로를 정의합니다.
#### **파일 업로드 API**:
- 클라이언트가 파일을 POST 방식으로 업로드할 수 있게 처리하는 `FileUpload` 클래스를 정의합니다.
- 파일이 없거나 선택되지 않은 경우 에러 메시지를 반환하고, 파일이 제대로 업로드되면 성공 메시지와 파일명을 반환합니다.
#### **애플리케이션 실행**:
- 스크립트가 직접 실행될 때, 모든 인터페이스와 포트 5000에서 웹 서버를 시작하고 디버그 모드를 활성화합니다.

### 3. Web Application 실행
- windows shell 상에서 `python video_analysis.py`를 실행하고 shell의 output stream을 통해 Flask web 서버가 정상적으로 기동된 것을 확인합니다.
- Url `http://localhost:5000/upload` 에 접속하여 upload page가 열리는지 확인합니다
- 해당 화면에서 임의의 파일을 선택해서 upload를 실행합니다.
- my_flask/upload 디렉토리에 upload한 파일이 존재하는지 확인합니다.

## STEP 2. File 정보를 데이터베이스에 저장
- 데이터베이스를 통해 업로드된 파일의 메타데이터를 저장하는 기능을 구현합니다.
- 참고 파일 : my_flask/video_analysis_05.py
### 1. 추가된 Code
```python

# 추가 : 데이터베이스 연동
from flask_sqlalchemy import SQLAlchemy
...
app = Flask(import_name=__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videodb.db'

api = Api(app, prefix="/api/v1")

db = SQLAlchemy(app)
...

# 추가 : 모델 정의
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_extension = db.Column(db.String(10), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Video {self.id}>"

# 추가 : 데이터베이스 초기화
with app.app_context():
    db.create_all()
...
class FileUpload(Resource):
    
    def post(self):
        ...

        # 추가 : 파일 정보를 데이터베이스에 저장
        video = Video(
            file_name=file.filename,
            file_extension=os.path.splitext(file.filename)[1],
            file_size=os.path.getsize(filename),
            created_at=db.func.now()
        )
        db.session.add(video)
        db.session.commit()
        ...
        return {'message': 'File uploaded successfully', 'filename': filename}, 201
```
### 2. Code 설명
#### **데이터베이스 연동**:
- `flask_sqlalchemy` 모듈을 사용해 SQLite 데이터베이스와의 연동 기능을 추가하였습니다.
#### **모델 정의**:
- 업로드된 비디오 파일의 메타데이터를 저장하기 위한 `Video` 모델이 정의되었습니다.
- 이 모델은 파일명, 파일 확장자, 파일 크기, 생성 날짜를 포함합니다.
- 각 업로드된 파일은 이 모델을 통해 데이터베이스에 저장됩니다.
#### **데이터베이스 초기화**:
- 스크립트 실행 시 `db.create_all()`을 호출하여 애플리케이션 컨텍스트 내에서 데이터베이스 스키마를 초기화합니다. 이는 정의된 모델에 기반한 테이블을 데이터베이스에 생성합니다.
#### **파일 정보를 데이터베이스에 저장**:
- 파일을 성공적으로 업로드한 후, 업로드된 파일의 메타데이터를 `Video` 모델 인스턴스로 생성하고, 이를 데이터베이스에 저장합니다.

### 3. Web Application 실행
- STEP 1의 Web Application 실행과정을 동일하게 수행합니다.
- my_flask/instance 디렉토리에 `videodb.db` 파일이 생성된 것을 확인합니다.
- sqlite viewer를 통해 `videodb.db`파일 내에 `Video` 테이블이 생성된 것을 확인합니다.

## STEP 3. File 정보를 데이터베이스에 저장
- 업로드한 비디오 파일의 목록을 웹 인터페이스와 API를 통해 조회할 수 있는 기능기능을 구현합니다.
- 참고 파일 : my_flask/video_analysis_06.py
### 1. 추가된 Code
```python

@app.route("/upload")
def upload():
    # 변경 : 파일 upload 후 비디오목록 page로 전환되도록 upload 템플릿 파일 변경
    return render_template('upload_06.html')

# 추가 : 비디오 파일 목록 page 라우트
@app.route("/videos")
def video_list():
    return render_template('videos_06.html')

# 추가 : 비디오 파일 목록 API 
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

api.add_resource(VideoList, '/videos')
```
### 2. Code 설명
#### **upload 템플릿 파일 변경**:
- 파일 upload 후 비디오 파일 목록 page로 전환되도록 upload 템플릿 파일을 변경합니다.
#### **비디오 파일 목록 page 라우트**:
- 업로드된 비디오 파일 목록을 보여주는 /videos라는 새로운 라우트가 추가되었습니다.
- 해당 페이지를 위한 템플릿 파일 `videos_06.html`을 설정했습니다.
#### **비디오 파일 목록 API**:
- 새로운 VideoList 클래스가 리소스로 추가되어, GET 요청을 통해 데이터베이스에 저장된 모든 비디오의 목록을 조회할 수 있는 API가 구현되었습니다. 
- 이 API는 각 비디오의 ID, 파일명, 파일 확장자, 파일 크기, 생성 날짜 등의 정보를 JSON 형식으로 반환합니다.

### 3. Web Application 실행
- windows shell 상에서 `python video_analysis.py`를 실행하고 shell의 output stream을 통해 Flask web 서버가 정상적으로 기동된 것을 확인합니다.
- Url `http://localhost:5000/upload` 에 접속하여 mp4 파일을 선택해서 upload를 실행합니다.
- 파일 upload 완료 후 `http://localhost:5000/videos` 경로로 자동 전환(Redirection)되고 방금 upload한 파일 정보가 조회됩니다.

## STEP 4. 비디오 분석 실행
- 특정 비디오 파일을 선택해서 분석(장면 분할 및 활동성 분석)을 실행합니다.
- 참고 파일 : my_flask/video_analysis_08.py
### 1. 추가된 Code
```python

# 추가 : 비디오 분석(자체 개발 함수) 모듈 가져오기
from functions import analyze_video

# 추가 : 비디오 분석 결과 모델 정의
class VideoSplit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    group_number = db.Column(db.Integer, nullable=False)
    min_frame_number = db.Column(db.Integer)
    max_frame_number = db.Column(db.Integer)
    frame_count = db.Column(db.Integer)
    start = db.Column(db.Float)
    duration = db.Column(db.Float)
    activity_intensity = db.Column(db.Float)
    min_similarity = db.Column(db.Float)
    min_frame_path = db.Column(db.String(255))
    max_frame_path = db.Column(db.String(255))

    def __repr__(self):
        return f"<VideoSplit {self.id}>"

@app.route("/videos")
def video_list():
    # 변경 : videos 템플릿 파일 변경
    return render_template('videos_07.html')

# 추가 : 비디오 분석 실행 API 
class VideoDetails(Resource):

    def post(self, video_id):
        # 여기에 비디오 분석 로직 추가
        # video_id로 video table에서 file_name을 읽음
        video = Video.query.get(video_id)
        if video is None:
            return {'error': 'Video not found'}, 404

        # 비디오 분석
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
                activity_intensity=group['activity_intensity'],
                min_similarity=group['min_similarity'],
                min_frame_path=group['min_frame_path'],
                max_frame_path=group['max_frame_path']
            )
            db.session.add(video_split)

        db.session.commit()

        return {'message': f'Video analysis completed and saved for video ID: {video_id}'}

api.add_resource(VideoDetails, '/video_details/<int:video_id>')
```
### 2. Code 설명
#### **비디오 분석(자체 개발 함수) 모듈 가져오기**:
- upload한 비디오 파일의 file system 경로를 입력하면 장면(take)별 분석결과를 return 하는 함수를 import합니다.
#### **비디오 분석 결과 모델 정의**:
- `VideoSplit이`라는 새로운 모델을 추가합니다.
- 이 모델은 업로드된 비디오를 분석한 결과를 저장하기 위한 것으로, 각 비디오가 어떻게 분할되었는지, 각 분할의 특정 프레임 번호, 시작 시간, 지속 시간, 활동 강도, 최소 유사도 등의 정보를 담고 있습니다.
#### **videos 템플릿 파일 변경**:
- 비디오 파일 목록의 각 열에 '분석 실행' 버튼이 추가되도록 videos 템플릿 파일을 변경합니다.
- 비디오 파일 목록의 각 열에 '분석 실행' 버튼이 추가됩니다.
- 해당 버튼을 클릭하면 `POST /api/v1/video_details/<video_id>`가 호출됩니다.
#### **비디오 분석 실행 API**:
- `VideoDetails`라는 새로운 리소스를 추가합니다.
- 이 리소스의 post 메서드는 특정 `video_id`에 대한 비디오 파일을 분석하는 로직을 포함하고 있습니다. 분석은 함수 `analyze_video`를 호출하여 수행됩니다.
- `analyze_video`에 의한 비디오 분석이 완료된 후, 그 결과는 `VideoSplit` 데이터베이스 테이블에 저장됩니다.

### 3. Web Application 실행
- STEP 3의 Web Application 실행과정을 동일하게 수행합니다.
- 비디오 파일 목록 화면에서 `분석 실행` 버튼을 클릭합니다.
- 분석 실행이 완료되면 sqlite viewer를 통해 `videodb.db`파일 내에 `VideoSplit` 테이블과 해당 테이블에 분석 결과가 생성된 것을 확인합니다.

## STEP 5. 비디오 분석 결과 조회
- 비디오 파일 분석 결과를 조회합니다.
- 참고 파일 : my_flask/video_analysis_09.py
### 1. 추가된 Code
```python
@app.route("/videos")
def video_list():
    # 변경 : videos 템플릿 파일 변경
    return render_template('videos_09.html')

class VideoDetails(Resource):
    ...

    # 추가 : 비디오 분석 결과 조회 API 
    def get(self, video_id):
        video_details = VideoSplit.query.filter_by(video_id=video_id).all()
        video_details_list = []
        for detail in video_details:

            # 소수 둘째 자리에서 반올림
            start_rounded = round(detail.start, 2)  
            duration_rounded = round(detail.duration, 2)
            activity_intensity_rounded = round(detail.activity_intensity, 2)
            min_similarity_rounded = round(detail.min_similarity, 2)

            video_details_list.append({
                'group_number': detail.group_number,
                'min_frame_number': detail.min_frame_number,
                'max_frame_number': detail.max_frame_number,
                'frame_count': detail.frame_count,
                'start': start_rounded,
                'duration': duration_rounded,
                'activity_intensity': activity_intensity_rounded,
                'min_similarity': min_similarity_rounded,
                'min_frame_path': detail.min_frame_path,
                'max_frame_path': detail.max_frame_path
            })
        
        return video_details_list
```
### 2. Code 설명
#### **videos 템플릿 파일 변경**:
- 비디오 파일 목록의 각 열에 '상세보기' 버튼이 추가됩니다.
- 해당 버튼을 클릭하면 `GET /api/v1/video_details/<video_id>`가 호출됩니다.
#### **비디오 분석 결과 조회 API **:
- `VideoDetails` 리소스에 GET API를 추가합니다.
- `VideoSplit`테이블로 부터 특정 `video_id`에 대한 비디오 파일 분석 결과를 조회합니다.

### 3. Web Application 실행
- STEP 4의 Web Application 실행과정을 동일하게 수행합니다.
- 비디오 파일 목록 화면에서 `상세보기` 버튼을 클릭합니다.
- 같은 화면에 해당 비디오 파일의 분석 결과가 조회됩니다.