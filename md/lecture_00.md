# 파이썬 소개!

![python_logo.png](/img/python_logo.png)

## Python 이란

- 1991년, 네덜란드 수학자 귀도 반 로섬(Guido van Rossum)이 발표한 인터프린터 언어로 오픈 소스입니다. 
- 1995년에 나온 java 보다도 먼저 나온 프로그래밍 언어입니다.

## Python 의 장점

- 코드가 짧다. 생산성이 좋다
- 개발이 쉽다.
- 방대한 라이브러리 ( beautifulsoup4, numpy, tensorflow 등)
- 가독성 
\- 간결하고 가독성이 좋다. 코드 블록을 이용한 들여쓰기로 구분
- 접착성
\- 기본적으로 제공되는 라이브러리 외에 외부 라이브러리를 추가할 수 있으며, C 언어로 되어 있는 모듈 또한 추가할 수 있음.
- 유니코드
\- 문자열을 유니코드로 표현하여, 한글, 중국어 등 영어가 아닌 문자에 대해서도 쉽게 다룰 수 있음. 
- 동적 타이핑 과 GC (Garbage Collection)
\- 파이썬 런타임 시 타입 체크를 하는 동시에 자동으로 메모리 관리

## 인터프리터 언어 vs 컴파일 언어

- 고급언어 : 사람이 이해하기 쉽도록 설계된 언어로서 컴퓨터 구조나 기능에 얽매이지 않음 
- 기계어 : 컴퓨터가 사용하는 언어

|    비교    |               인터프리터 언어               |                                컴파일러 언어                                 |
| :--------: | ------------------------------------------- | ---------------------------------------------------------------------------- |
|    특징    | • 코드를 한 줄씩 번역 및 실행               | • 프로그램 단위로 번역하여 실행파일을 생성하는 과정(빌드과정)을 거친 후 실행 |
|    장점    | • 코드 변경시 빌드 과정없이 바로   실행가능 | • 실행 속도가 빠르고, 보안성이 높음                                          |
|    단점    | • 실행   속도가 느림                        | •  소스코드를 기계어로 번역하는 빌드 과정이 느림                             |
| 관련  언어 | • Python,   Javascript,   Ruby, PHP         | • C, C++, Java, C#, Go                                                       |

## Python 활용분야

- 시스템 유틸리티 제작
- GUI 프로그래밍
- 업무자동화
- web 프로그래밍 - django, flask
- data 분석 - Numpy, Pandas, Matplotlib
- 머신러닝  - Scikit-Learn,  TensorFlow
- 사물 인터넷 - Raspberry Pi

- 파이썬과 어울리지 않는 분야
  - 시스템과 밀접한 프로그래밍 영역. 빠른속도를 요구하거나 하드웨어를 직접 건드리는 프로그램
  - 모바일 프로그램

- [What do you use Python for?](https://www.jetbrains.com/research/python-developers-survey-2018/)
- [카이스트 공익 사례](https://www.clien.net/service/board/park/12883515)

## Anaconda 

- **Anaconda 란? ( 파이썬 + 여러 패키지)**
파이썬 / R 데이터 과학 및 기계 학습을 수행하기 위한 수학, 과학 분야의 패키지
(Numpy, SciPy, IPython, Matplotlib..) 를 포함하는 오픈소스
최근에는 인공지능이나 데이터 분석을 위해 파일썬을 많이 사용하여, 아나콘다를 설치하고 시작하는 경우가 많음

  - Anaconda Python 3.7 버전 설치
    DownLoad ::  <https://www.anaconda.com/distribution/>
  - Anaconda Prompt 실행
    윈도우 시작 -> Anaconda Prompt 검색 -> Anaconda Prompt 실행
  - Proxy 설정
    1. Anaconda Prompt 에서 아래 명령어 실행

       ```bash
       conda config --set ssl_verify False
       ```

    2. `<USER HOME>` (C:\Users\SDS) 에 .condarc 라는 파일이 생성됨.
    3. .condarc 파일을 아래와 같이 편집

       ```bash
       proxy_servers:
         http: http://70.10.15.10:8080
         https: http://70.10.15.10:8080 
       ```

## Jupyter notebook

- Jupyter 란?

  아나콘다 환경을 웹에서 사용할 수 있도록 연결해 주는 오픈 소스 웹 어플리케이션으로 라이브코드, 등식,
 시각화화 설명을 위한 텍스트 등을 포함한 문서를 만들고 공유할 수 있습니다. 
 실시간으로 인터렉티브하게 데이터를 조작하고 시각화 할 수 있다는 점이 가장 큰 장점입니다. 

- Jupyter 설치
  Anaconda Prompt 에서 아래 명령 실행

    ```bash
    conda install -c conda-forge jupyter_contrib_nbextensions
    ```

- Jupyter 실행
  1. Anaconda Prompt 에서 실행하고자 하는 폴더에서 아래 명령어 실행

    ``` bash
    jupyter notebook
    ```

  2. jupyter notebook 이 실행되면 자동으로 기본 브라우저가 실행되어 jupyter notebook [http://localhost:8888](http://localhost:8888)에 접속
  3. 4번째 Tab 인 Notebook extension 선택
  4. Extension 체크

       - Execute Time
       - Live Markdown Preview
       - Move selected cells
       - Table of Contents(2)
       - table_beautifier

  - Jupyter Notebook 단축키
    -명령모드(Command Mode)와 편집모드(Edit Mode)
    - Command Mode : Cell 이동 및 생성삭제
![command_mode.png](/img/command_mode.png)


      - 편집모드로 전환 : Esc 키
      - Cell 타입 변경 (마크다운 / Code)
        - Markdown Cell : m
        - Code Cell : y
      - Cell 추가
        - Cell 위에 추가 : a ( add a cell above)
        - Cell 아래에 추가 : b ( add a cell below)
      - Cell 삭제
        - 1개 Cell 삭제 : dd (d 연속 2번 입력)
        - 여러 Cell 삭제 : Shift + 화살표키로 영역 선택 -> dd
      - Cell 복사
        - 현재 cell 복사 : c
      - Cell 붙이기
        - 현재 cell 아래 붙여넣기 : v (소문자 v)
        - 현재 cell 위 붙여넣기 : V (대문자 v)
      - Cell 작업 취소 : z
    - Edit Mode : Cell 내의 내용을 편집
![edit_mode.png](/img/edit_mode.png)
      - ESC : 명령모드로 전환
      - 동시편집 : CTRL 누른 상태에서 원하는 위치 클릭후 편집
      - 단어별 이동 : CTRL 누른 상태에서 화살표 이동
      - 주석처리 : CTRL + /
