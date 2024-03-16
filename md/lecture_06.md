# Generator, 예외처리

## 제너레이터

- 제너레이터는 이터레이터를 생성해 주는 함수. yield 키워드를 사용한다.
- 내장 컨테이너 자료형은 iterator를 내장하고 있으며 다음과 같이 접근하여 사용 가능하다.
  
  ``` python
  list_iter = iter([1,2,3])

  print(next(list_iter))
  print(next(list_iter))
  print(next(list_iter))
  print(next(list_iter))
  ```

- for문의 원리는 내장 컨테이너 자료형의 iterator객체를 StopIteration예외가 날때까지 next()를 계속호출하는 것.
- 결과를 return하는 일반함수는 이터레이터가 생성되지 않는다.

  ``` python
  # 일반함수
  def tmp_function():
      print('in tmp_function')

  f_itr = iter(tmp_function())  # not iterable 오류 발생
  ```

- 제너레이터는 iterator가 생성되며 yield가 호출되는 만큼 next가 호출된다.
- 아래의 코드를 실행하면 next가 호출되면 다음 yield를 만날때까지 제너레이터를 진행하고 yield가 반환된 후 다음 next가 호출될 때까지 제너레이터는 대기하고 있음을 알 수 있다.

  ``` python
  def tmp_generator():
      print('in tmp_generator : before first')
      yield 'fisrt'
      print('in tmp_generator : before second')
      yield 'second'
      print('in tmp_generator : before third')
      yield 'third'
      print('in tmp_generator : end')
  
  g_itr = iter(tmp_generator())
  print('-- start looping generator --')
  print(next(g_itr))  # first
  print(next(g_itr))  # second
  print(next(g_itr))  # third
  print(next(g_itr))  # StopIteration
  ```

## 제네레이터 사용

- 제너레이터 함수

  ``` python
  def double(size):
      for i in range(size):
          yield i*2

  dob_gen = double(10)
  
  for i in dob_gen:
      print(i)
  ```

- generator 함수를 좀 더 쉽게 사용할 수 있도록 generator expression 을 제공
- list comprehension 과 비슷하지만 [ ] 대신 ( ) 을 사용

  ```python
  # list comprehension
  com = [i*2 for i in range(5)]
  # generator
  gen = (i*2 for i in range(5))
  print(com)
  print(gen)
  ```

- 메모리 확인

  ```python
  import sys
  print(sys.getsizeof(com))
  print(sys.getsizeof(gen))
  ```

## 제너레이터 예제

- generator와 comprehension 피보나치 수열 만들기 비교

  ``` python
  # 제너레이터로 피보나치 수열 List만들기
  def fib(n):
      f0, f1 = 0, 1
      for i in range(1, n+1):
          f0, f1 = f1, f0 + f1
          yield f0

  for res in fib(10):
      print(res)
  ```

## 예외처리

- try / except 구문을 사용
- 예외처리 문 기본구조

  ```python
  try:
      수행코드
  except 에러이름 as 메세지변수:
      에러처리
  except 에러이름 as 메세지변수:
      에러처리
  else:
      에러가 발생하지 않을 경우 수행
  finally:
      에러발생여부 상관없이 항상 수행
  ```

  ```python
  def divide(a, b):
      return a / b

  try:
      c = divide(5, num2)
  except ZeroDivisionError:
      print('두 번째 인자는 0이여서는 안됩니다.')
  except NameError:
      print('정의되어 있지 않은 변수입니다.')
  except TypeError:
      print('숫자로 입력하여 주세요')
  else:
      print(f'결과는 {c}입니다.')
  finally:
      print('계산이 완료되었습니다')
  ```

- 강제로 에러를 발생시킬 경우
  - raise 구문을 사용

  ```python
  def raise_error_func():
      raise NameError

  try:
      raise_error_func()
  except NameError:
      print ("NameError occrued")
  ```

- 사용자 정의 예외
  - Exception 을 상속받아 새로운 예외 생성

  ```python
  class NegativeDivisionError(Exception):
      def __init__(self, value):
          self.value = value

  def positive_divide(a, b):
      if ( b < 0):
          raise NegativeDivisionError(b)
      return a / b

  try:
      result = positive_divide(10, -1)
  except NegativeDivisionError as e:
      print(f'두번째 인자는 양수여야 합니다. :: {e.value}')
  ```