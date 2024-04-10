## Flask-SQLAlchemy 란?
Flask-SQLAlchemy는 Flask와 SQLAlchemy의 강력한 기능을 결합하여, Flask 웹 애플리케이션에서의 데이터베이스 작업을 효율적이고 간편하게 만들어 줍니다. ORM을 통한 데이터베이스 작업의 추상화는 애플리케이션 개발의 생산성을 크게 향상시킬 수 있습니다. Flask-SQLAlchemy를 사용함으로써, 개발자는 데이터베이스 작업을 보다 직관적으로 처리할 수 있게 되며, Flask 애플리케이션의 전반적인 개발 과정을 더욱 간소화할 수 있습니다.

## 주요 특징

- **간결한 구성**: Flask 애플리케이션에 쉽게 통합할 수 있으며, 몇 줄의 코드만으로 데이터베이스 설정이 가능합니다.
- **자동 세션 관리**: 데이터베이스 세션 관리를 자동으로 처리해 주어, 수동으로 세션을 열고 닫을 필요가 없습니다.

## 설치 및 기본 사용법

Flask-SQLAlchemy를 사용하기 위해서는 먼저 패키지를 설치해야 합니다.

```
pip install Flask-SQLAlchemy
```

이후, Flask 애플리케이션에 Flask-SQLAlchemy를 설정합니다.

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(import_name=__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///videodb.db'
db = SQLAlchemy(app)
```

## 모델 정의

데이터베이스 테이블과 매핑될 모델(클래스)를 정의합니다.

```python
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_extension = db.Column(db.String(10), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
```

## 데이터베이스 작업

모델을 통해 데이터베이스에 쿼리를 실행하거나, 데이터를 추가, 수정, 삭제할 수 있습니다.

```python
#Video 파일 정보를 데이터베이스에 저장
video = Video(
    file_name='video',
    file_extension='.mp4',
    file_size=os.path.getsize(filename),
    created_at=db.func.now()
)

db.session.add(video)
db.session.commit()

# Video 조회
video = Video.query.get(video_id)
print(video.file_name)

# Video 삭제
db.session.delete(video)
db.session.commit()
```