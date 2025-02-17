## Flask 란?
Flask는 Python으로 작성된 가벼운 웹 애플리케이션 프레임워크입니다. Flask는 간단하면서도 확장 가능한 웹 애플리케이션을 구축하는 데 필요한 기본 도구를 제공합니다. Flask를 사용하면 웹 서버, 템플릿 렌더링, 라우팅 등의 기능을 쉽게 구현할 수 있습니다.

## 설치
Flask는 pip를 사용하여 설치할 수 있습니다. 터미널이나 커맨드 프롬프트에서 다음 명령어를 입력하면 Flask가 설치됩니다.
```
pip install Flask
```

## 코드 구성
### 1. 기본 애플리케이션
Flask 애플리케이션을 시작하는 가장 간단한 형태는 몇 줄 안 되는 코드로 구성됩니다.

```python
from flask import Flask

app = Flask(import_name=__name__)

@app.route("/")
def home():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```
위 코드는 가장 기본적인 Flask 애플리케이션 구조를 보여줍니다. 여기서 `@app.route('/')` 데코레이터는 URL 경로를 함수에 매핑합니다. 이 경우, 루트 URL (`'/'`)이 `home` 함수에 매핑되어, 해당 경로에 접속하면 'Hello, World!'라는 메시지를 반환합니다.

### 2. 라우팅
Flask에서 라우팅은 클라이언트의 요청을 적절한 핸들러 함수에 연결하는 과정입니다. `@app.route` 데코레이터를 사용하여 경로와 함수를 연결합니다.

```python
@app.route('/home')
def home():
    return '<p>Hello, World!</p>'
```

### 3. 변수 규칙
경로에 변수 부분을 추가하여 동적 URL을 생성할 수 있습니다. 변수 부분은 꺾쇠(`<`, `>`)로 감싸서 표시합니다.

```python
@app.route('/home/<username>')
def home(username):
    # 사용자에 대한 정보를 보여주는 페이지
    return f'{username}님 환영합니다.'
```

### 4. 템플릿 렌더링
Flask에서는 Jinja2 템플릿 엔진을 사용하여 템플릿을 렌더링할 수 있습니다. 템플릿을 사용하면 HTML 파일 내에서 Python 코드를 사용할 수 있습니다.

```python
from flask import render_template

@app.route("/home/<username>")
def home(username):
    return render_template('index.html',title=f'{username}님 환영합니다.')
```
위 코드에서 `render_template` 함수는 `index.html` 템플릿 파일을 렌더링하며, `name` 변수를 템플릿에 전달합니다.

### 5. 실행 및 디버그
```python
app.run(host="0.0.0.0", port=5000, debug=True)
```
- `app.run()` : Flask 서버를 시작합니다. 
- `host='0.0.0.0'` : 애플리케이션을 서버의 모든 네트워크 인터페이스에 바인딩합니다.
- `port=5000` : 애플리케이션의 접근 포트를 지정합니다.
- `debug=True` : 디버그 모드를 활성화하여 개발 중에 발생할 수 있는 오류를 더 쉽게 추적하고, 코드 변경 시 자동으로 애플리케이션을 재시작하게 합니다.

## 디렉토리 구조
```bash
/my-flask
    /static
        capture_1.png
    /templates
        index.html
        upload.html
        vidoes.html
    /instance
        videodb.db
    /upload
        SampleVideo_640x360_5mb.mp4
    video_analysis.py

```
- `/static`

    CSS 파일, JavaScript 파일, 이미지 파일과 같은 정적 파일을 저장하는 곳입니다.
- `/templates`

    HTML 템플릿 파일을 저장하는 곳입니다. Flask에서는 Jinja2 템플릿 엔진을 사용하여 동적인 웹 페이지를 생성할 수 있습니다. 이 디렉터리 내의 템플릿 파일들은 Flask 애플리케이션에서 render_template() 함수를 통해 렌더링될 수 있습니다.
- `/upload`

    사용자가 업로드한 파일을 저장하는 곳입니다.
- `/instance`

    배포 단위로 변경(Deployment Specific)되는 정보 또는 보안상 민감한 정보(예: 데이터베이스 파일, 설정 파일 등)를 저장하는 곳입니다.
- `video_analysis.py`

    Flask 애플리케이션의 메인 파일로, 라우트와 뷰 함수를 정의합니다. `app.run()` 함수를 호출하는 code를 담고 있습니다.

## Flask 애플리케이션 실행
터미널이나 커맨드 프롬프트에서 app.py 파일이 있는 디렉터리로 이동한 후, 다음 명령어를 사용하여 Flask 애플리케이션을 실행합니다.

```bash
python video_analysis.py
```