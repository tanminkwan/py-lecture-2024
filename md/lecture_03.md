# 조건문, 반복문

## 문법

- if / for / while 은 기본적으로 아래와 같이 :(콜론) 으로 정의한다.

- 안의 statement(수행문장)은 항상 들여쓰기를 해야 한다.

  ```python
  if < 조건문 > :
      statement
  ```

  ```python
  for < 조건문 > :
      statement
  ```

  ```python
  while < 조건문 > :
      statement
  ```

## 들여쓰기 (indent)

- 파이썬은 문법상 블록 지정을 들여쓰기로 한다.
- 파이썬은 공백, 탭 문자를 통해 들여쓰기가 가능하지만 **`공백4개 사용을 권장한다.`**

  ``` java
    // Java에서의 블록 지정 예
  if(true)
  {
      System.out.println(true);
  }
  ```

  ``` python
  # python에서 블록 지정
  x = 2

  if x == 2:
      print(x)  # 들여쓰기를 해주어야 정상 작동
      print(x+1)
  ```

- if, for, while등 문법 맨 뒤에 `:` 가 들어갔을 때 들여쓰기를 하지 않으면 오류 발생

- 일관성 없는 들여쓰기를 사용해도 오류 발생
  
  ``` python
  if x == 2:
  print(x)  # if문 아래 들여쓰기 안한 경우 IndentationError 발생

  if x == 2:  # if문 아래 일관성 없는 들여쓰기
      print(x)  # 4칸 들여쓰기
    print(x+1)  # 2칸 들여쓰기 : indentationError 발생
  ```

## 조건문

- Java의 else if() 문이 파이썬에서는 `elif` 이다.

  ``` python
  if x < 0:
      x = 0
      print('Negative changed to zero')
  elif x == 0:
      print('Zero')
  elif x == 1:
      print('Single')
  else:
      x=15
      print('More')  
  # More 이 출력된다.
  ```

- 중첩 조건문

  ``` python
  if x >= 10:
      print('10이상입니다.')
      if 15 <= x < 20:  # x >= 15 and x < 20 을 이렇게 표현할 수 있다.
          print('15이상 20미만 입니다.')
      elif x == 20:
          print('20입니다.')
  ```

- 조건문 empty 블록
  pass를 사용해서 empty 구문을 지정할 수 있다.

  ``` python
  if x <= 15:
      pass  # pass를 넣지 않으면 indentationError발생
  else:
      print('15보다 크거나 같다')
  ```

- 조건부 표현식 (3항 연산자)
  Java의 3항 연산자와 비슷한 표현식을 제공한다.

  ``` Java
  // Java
  int x = 15;
  System.out.println(x >= 0 ? "0이상" : "음수");
  ```

  ``` python
  # python
  print('0 이상' if x >= 0 else '음수')
  ```

## 반복문

- while

  ``` python
  n = 5
  while n > 0:
      n -= 1
      print(' '*n, '*'*(1+(4-n)*2), ' '*n)
  else:
      print('end print stars')
  ```

- for
  
  - for 문 기본구조

    ```python
    for 변수 in 반복가능한 객체 iterable:
        statement
    ```

  - iterator를 차례대로 접근한다.

    ``` python
    import random
    strike, ball = 0, 0

    for i in range(7):
        rand_i = random.randint(0, 1) # 0부터 1 사이의 임의의 정수

        if rand_i == 1:
            strike += 1
        else:
            ball += 1

        print(ball, 'balls', strike, 'strikes')

        if strike == 3:
            print('strike out')
            break

        if ball == 4:
            print('four-ball')
            break
    ```

  - 내장 컨테이너 자료형의 Iteration

    - for 문은 내부적으로 iterable 에서 iterator 를 만들어내어 하나씩 꺼내서 반복
    - iterable vs iterator
      - iterable : 반복 가능한 객체
        - `__iter__()` 메서드 구현. iterator 생성

      - iterator : iterable 하며, 값을 차례대로 하나씩 꺼낼 수 있는 객체
        - `__next__()` 메서드 구현. 다음 항목을 리턴
        - `__iter__()` 메서드 구현. self 리턴

      ``` python
      # list
      rand_int_list = []
      for i in range(10):
          rand_int_list.append(random.randint(1,10))
  
      print(type(rand_int_list))
      print(dir(rand_int_list))
      print(iter(rand_int_list))
  
      for int_v in rand_int_list:  # list iterator
          print(int_v, end=', ')
  
      # tuple
      rand_int_tuple = tuple(rand_int_list)
      print(type(rand_int_tuple))
      print(dir(rand_int_tuple))
      print(iter(rand_int_tuple))
  
      for int_v in rand_int_tuple:  # tuple iterator
          print(int_v, end=', ')
  
      # set
      rand_int_set = set(rand_int_tuple)  # 중복 사라짐
      print(type(rand_int_set))
      print(dir(rand_int_set))
      print(iter(rand_int_set))
  
      for int_v in rand_int_set:  # set iterator
          print(int_v, end=', ')
  
      # dictionary
      rand_int_dict = dict.fromkeys(rand_int_set)  # value가 None인 dictionary
      print(type(rand_int_dict))
      print(dir(rand_int_dict))
      print(iter(rand_int_dict))
  
      for int_v in rand_int_dict:  # dict iterator. key만 출력된다.
          print(int_v, end=', ')
  
      for key, value in rand_int_dict.items():  # key, value모두 출력시 items()함수를 이용.
          print(key, value, end=', ')
      ```

## enumerate(), zip()

- enumerate(iterable, start = 0) 함수는 start부터 시작하는 인덱스 값을 포함하는 enumerate 객체를 리턴

  ``` python
  print(list(enumerate(rand_int_list)))  # tuple의 list형태이다.
  for idx, int_v in enumerate(rand_int_list):
      print(idx, int_v)
  ```

- zip(*iterable) 함수는 n개의 자료형을 묶어 zip객체를 리턴. 가장 짧은 자료형의 길이 zip객체의 길이가 된다.

  ``` python
  rand_char_list = []

  for i in range(10):
      rand_char_list.append(chr(random.randint(65,90)))

  print(rand_char_list)
  print(list(zip(rand_int_list, rand_char_list)))  # tuple의 list형태이다.

  # zip을 이용한 dict 생성
  dict_by_zip = dict(zip(rand_int_list, rand_char_list))  # key의 중복은 삭제된다.

  for key, value in dict_by_zip.items():  
      print(key, value, sep=':', end=', ')

  # list 2개 이상 한번에 for 문을 돌릴 때
  team = ['A', 'B', 'C', 'D']
  country = ['Korea', 'America', 'France', 'China']
  player = ['kim', 'hans', 'guillaume', 'cheng']

  for a1, a2, a3 in zip(team, country, player):
      print(f"소속 {a1} / 국가 {a2} / 이름 {a3}")
  ```