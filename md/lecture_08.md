# Package

## modules

- 모듈이란 함수나 변수 또는 클래스 들을 모아 놓은 파일
- 파이썬은 다양한 모듈 제공
- 문자열(string), 랜덤(random), 파일(file), 수학(math), 날짜(date), 시간(time) 등

  ```python
  # 사용법
  # mod.py 안에 square 라는 함수가 있는 경우
  
  # 1. import 모듈이름
  import mod
  print(mod.square(2,3))
  
  # 2. from 모듈이름 import 함수이름
  from mod import square
  print(square(2,3))
  
  # 3. from 모듈이름 import 함수이름 as 별칭
  from mod import square as s
  print(s(2,3))
  
  # class 의 경우도 마찬가지이다.
  import mod
  a = mod.Bread()
  print(a.intro())
  
  from mod import Bread
  a = Bread()
  print(a.intro())
  
  # 현재 경로
  import os
  os.getcwd()
  
  # The Zen of Python
  import this
  ```
## PEP 8
  - [PEP 8](https://www.python.org/dev/peps/pep-0008/)(Python Enhancement Proposals 8) 파이썬 코딩 스타일 가이드
  - [PEP 8 key guideline](https://realpython.com/python-pep8/)

## PIP

- 파이썬으로 작성된 패키지 라이브러리를 관리하는 시스템
- 패키지 설치

  pip install <패키지 이름>

  ```bash
  // pip list
  pip list
  // pip install 패키지
  pip install numpy
  // pip uninstall 패키지
  pip uninstall numpy
  ```

## Conda
- 아나콘다에서는 conda 로 패키지 라이브러리를 관리
- 패키지 설치

  conda install <패키지 이름>

  ```bash
  // conda list
  conda list
  // conda install 패키지
  conda install numpy
  // conda uninstall 패키지
  conda uninstall numpy
  ```
## 패키지들..

- beautiful soup, Selenium
- pandas, numpy