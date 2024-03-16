# Hello python 문자형 숫자형 bool형

## Hello python 출력해 보기

  ``` python
  # python
  print('hello world')
  ```

  ``` java
  // Java
  public class Test {
      public static void main(String[] args) {
          System.out.println("Hello World");
      }
  }
  ```  

## 변수선언
  
- 변수 작명 스타일
  - snake_case
  - 숫자, 문자, _ 만 허용.
  - 첫글자는 숫자가 될 수 없다.
  - 예약어는 피해서 사용하도록 한다. (object is not callable 오류 발생 위험 있음)
       [Built-in Functions](https://docs.python.org/3/library/functions.html "Built-in Functions")
  - Case Sensitive

    ``` python
    hello_python = 'hello python'
    number_var = 33
    5_eggs = 20  # SyntaxError: invalid syntax
    empty_var = None  # null
    ```

- 변수 한번에 선언하기
  
  ``` python
  first, second, third = 1, 2, 3
  ```

- 변수 swap
  
  ``` python
  second, third, first = first, second, third
  ```

## 주석처리
  
- \# 뒤의 문장은 주석으로 처리된다.
- 여러 줄의 주석을 처리하기 위해서 ''' 와 ''' 또는 """ 와 """ 로 감싼다. (docstring)
  
  ``` python
  # 주석처리 된 문자

  '''
      여러 줄에 걸쳐서
      주석을 처리한다.
  '''

  """
      이것 또한 주석 처리된
      문장입니다.
  """
  ```

## 숫자형

- 숫자 형태로 이루어진 자료형. 정수, 실수, 8진수, 16진수가 있다.
     항목  |         사용 예
    ------ | -----------------------
    정수   | 335
    실수   | 114.78
    8진수  | 0o75
    16진수 | 0x5F

- 연산자
  
    ``` python
  a = 6
  b = 4
  a+b  # 덧셈
  a-b  # 뺄셈
  a*b  # 곱셈
  a/b  # 나눗셈
  a//b  # 몫
  a%b  # 나머지
  a**b  # a^b
  divmod(a,b)  # 몫과 나머지 동시계산
    ```

- 형변환
  string → int

    ``` python
    str_var = '5123'
    int_var = int(str_var)

    type(int_var)
    ```

- 진수변환

    ``` python
    int('FC', 16)  # 16진수 → 10진수
    int('76', 8)  # 8진수 → 10진수
    int('110', 2)  # 2진수 → 10진수

    hex(252)  # 10진수 → 16진수
    oct(62)  # 10진수 → 8진수
    bin(6)  # 10진수 → 2진수
    ```

- ASCII 변환

    ``` python
    ord('A')  # 문자 → ASCII
    ord('a')  # 문자 → ASCII

    chr(65)  # ASCII → 문자
    chr(97)  # ASCII → 문자
    ```

## 문자열 자료형

- 문자열 선언방법
  큰따옴표를 양쪽을 둘러 싸거나 작은따옴표로 양쪽을 둘러싼다.

    ``` python
    str1 = "안녕하세요"
    str2 = '반갑습니다'
    ```

  "" 로 선언한 경우 문자열이 '를 포함할 수 있고 ''로 선언한 경우 문자열이 "를 포함할 수 있다. escape(\\) 문자를 써서도 포함할 수 있다.

    ``` python
    str1 = "I'm fine."
    str2 = 'He said. "I\'m tired"'
    ```

  여러 줄인 문자열을 변수에 대입하려면 ''' 또는 """를 이용한다.

    ``` python
    multi_line_str = '''
        이름: 김슬아
        직급: 프로
        소속: 금융실행그룹
    '''

    multi_line_str2 = """
        이름: 김슬아
        직급: 프로
        소속: 금융실행그룹
    """
    ```

- 문자열 연산

    ``` python
    head = 'python '
    tail = 'language'

    concat_str = head + tail
    multi_str = head * 3
    ```

- 문자열 인덱싱
  문자열 인덱싱은 문자열의 특정 위치의 값을 뽑아내는 것을 말한다.
  파이썬은 0 base index를 사용한다.

    ``` python
    korea = '대한민국'
    korea[1]
    korea[-1]
    ```

- 문자열 슬라이싱
  문자열 슬라이싱이란 문자열에서 특정 위치의 문자열을 뽑아내는 방법.

     ``` python
    anthem = '동해물과 백두산이 마르고 닳도록'
    anthem[0:4]  # 0이상 4미만 슬라이싱
    anthem[10:]  # 10이상부터 끝까지 슬라이싱
    anthem[:9]   # 처음부터 9미만 슬라이싱
    anthem[:]    # 전체문자열
    anthem[5:-4] # 5이상 부터 끝에서 4번째 전 미만 슬라이싱 == anthem[5:len(anthem)-4]

    number = '0123456789'
    number[::2]    # 2칸씩 띄어서 슬라이싱
    number[1::2]   # 1이상부터 2칸씩 띄어서 슬라이싱
    number[2:8:2]  # 2이상부터 8미만까지 2칸씩 띄어서 슬라이싱
    number[::-1]   # 전체문자열 reverse
    number[-1:3:-2]# 에서부터 반대로 2칸씩 3초과까지 슬라이싱
    ```

- 문자열 포매팅
  문자열 내에 또 다른 문자열을 삽입하기 위한 방법

    ``` python
    # C 스타일의 문자열 포매팅
    '류현진의 올해 방어율은 %.2f이다.' % 2.0358

    '손흥민의 소속팀은 %s이다.' % '토트넘' 

    '류현진의 소속팀은 %s이며 %d년에 입단했다.' % ('LA 다저스', 2013)

    # format 함수를 이용한 포매팅
    '{}는 전직 국가대표 피겨스케이팅 선수이다.'.format('김연아')

    '{0}는 {1}년 {2} 동계올림픽에서 금메달을 획득했다.'.format('김연아', 2010, '벤쿠버')

    '{name}은 전직 야구선수로 KBO 통산 홈런 갯수는 {homerun}개 이다.'.format(homerun=467, name='이승엽')  # 이승엽은 전직 야구선수로 KBO 통산 홈런 갯수는 467개 이다.

    '{0:!^5}의 KBO 통산 타율은 {1:.3f}이다.'.format('이승엽', 0.3022994)

    # f문자열 포매팅
    player_name = '박찬호'
    nickname = 'too much talker'
    birth = 1973

    f'{player_name}는 전직 야구선수로 {2019-birth}살 이고 별명은 {nickname:☆^17}이다.'
    ```

- 문자열 함수들

    ``` python
    players = '류현진,손흥민,김연아,이승엽,박찬호 '

    len(players)  # 문자열 길이

    players_list = players.split(',')  # 문자열 리스트로 나누기

    ', '.join(players_list)  # list항목들을 ,로 구분하며 합친다.

    players.count(',')  # ,의 갯수

    players.find('이')  # '이'가 처음나온 위치

    players.strip()  # 양쪽 공백 제거 (lstrip, rstrip)

    players.replace(',', '/')  # 문자열 바꾸기

    players.startswith('류현진')  # 시작문자 여부 확인

    players.endswith("박찬호 ")  # 종료문자 여부 확인

    'a'.upper()  # 대문자로 바꾸기 : A
    'A'.lower()  # 소문자로 바꾸기 : a
    ```

## bool 자료형

- 참과 거짓을 나타낸다.
    참 : True / 거짓 : False (맨 앞 글자가 대문자임을 유의)
    문자열, 리스트, 튜플, 딕셔너리등의 값이 비어있으면 거짓.

     값    | Bool
    -------- | -----
    'python' | True
    ''       | False
    [1,2]    | True
    []       | False
    ()       | False
    {}       | False
    9        | True
    0        | False
    None     | False

- 비교 연산자

    ``` python
    # 값 비교
    1000000007 == 1000000007
    1000000007 > 1000000007
    'Python' == 'Python'
    'Java' != 'Java'

    # 객체 비교
    comp1, comp2 = [103, 104] , [103, 104]
    comp1 == comp2  # 값 비교
    comp1 is comp2  # 레퍼런스 비교
    id(comp1)
    id(comp2)
    ```

- 논리 연산자
    Java(&&, ||, !)와는 다르게 파이썬은 논리 연산자를 and, or, not으로 사용한다.

    ``` python
    10 == 10 and 10 != 5
    10 > 5 or 10 < 3
    not 10 > 5
    ```

- 연산자 우선순위
    우선순위 |      연산자      |    설명
    -------- | ---------------- | -----------
    1        | is, <, >, !=, == | 비교 연산자
    2        | not x            | 논리 not
    3        | and              | 논리 and
    4        | or               | 논리 or

    ``` python
    not 1+1==2 or 4==4 and 7==8

    (not 1+1==2) or 4==4 and 7==8
    (not 1+1==2) or (4==4 and 7==8)
    ```