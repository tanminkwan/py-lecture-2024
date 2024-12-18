## Flask-RESTful 이란?

Flask-RESTful은 Flask를 확장하여 RESTful 웹 서비스를 구축할 수 있게 해주는 라이브러리입니다. Flask-RESTful을 사용하면 Python과 Flask의 간결함을 유지하면서도 RESTful API를 쉽게 구축할 수 있습니다.

## Flask-RESTful 설치
먼저, Flask-RESTful을 사용하기 위해 설치해야 합니다. Flask가 이미 설치되어 있다고 가정하고, 다음 명령어로 Flask-RESTful을 설치합니다.
```
pip install flask-restful
```

## 기본 애플리케이션 구조
Flask-RESTful을 사용하여 기본적인 REST API를 구축하는 과정을 살펴보겠습니다.

### 1. 애플리케이션 설정
```python
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
```
여기서, `Api(app)`을 통해 Flask 애플리케이션에 Flask-RESTful API를 연결합니다.

### 2. API 인스턴스 생성 시 Prefix 추가

`Api` 인스턴스를 생성할 때 `prefix` 매개변수를 사용하여 전체 API에 적용될 공통 접두어를 지정할 수 있습니다. 예를 들어, API의 첫 번째 버전을 만들고 있다면, 모든 리소스 경로 앞에 `/api/v1`을 추가할 수 있습니다.

```python
api = Api(app, prefix='/api/v1')
```

이 설정을 통해 추가하는 모든 리소스 경로 앞에 자동으로 `/api/v1`이 붙게 됩니다. 예를 들어, `/todos` 경로로 `TodoList` 리소스를 추가한다면 실제 경로는 `/api/v1/todos`가 됩니다.

### 3. 리소스 정의
RESTful 서비스에서 '리소스'는 API를 통해 액세스되는 객체나 정보를 의미합니다. Flask-RESTful에서는 리소스를 클래스로 정의합니다. 각 메서드(get, post, put, delete 등)는 HTTP 메서드에 해당합니다.

```python
from flask_restful import Resource

class HomeAPI(Resource):
    def get(self):
        return {'hello': 'world'}
```

### 4. 리소스 추가
정의한 리소스를 API에 추가하고, 경로를 지정합니다.

```python
api.add_resource(HomeAPI, '/home')
```

## 리소스에 메서드 추가
Flask-RESTful에서 리소스는 API의 엔드포인트와 연결된 클래스입니다. 클래스 내에 HTTP 메서드에 해당하는 메서드(get, post, put, delete 등)를 정의하여 리소스를 관리할 수 있습니다.

```python
class HomeAPI(Resource):

    def get(self, username):
        message = f'{username}님 환영합니다.'
        return {'result': message}, 200

    def put(self, username):
        # do something
        return {'username': username}, 200
```

## URI 변수 사용
경로 변수를 사용하여 동적 URI를 만들 수 있습니다. 변수는 함수의 인자로 전달됩니다.

```python
api.add_resource(HomeAPI, '/home/<string:username>')
```