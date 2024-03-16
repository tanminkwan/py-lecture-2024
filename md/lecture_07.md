# Closure, Decorator

## Scope

- 지역변수와 전역변수
  ``` python
  num = 10

  def lucky_num():
      num = 7
      print(num)

  lucky_num()
  print(num)
  ```


- 함수 안에서 전역변수 바꾸거나 선언하기
  - `global` 키워드를 사용
  ``` python
  gnum = 10

  def change_num():
      global gnum
      gnum = 11
      global new_gnum
      new_gnum = 30

      print(gnum)
      print(new_gnum)

  change_num()
  print(gnum)
  print(new_gnum)
  ```

- 중첩 함수의 Scope

  ``` python
  def korean():
      name = 'KIM'

      def lee():
          name = 'LEE'
          print(name)

      lee()
      print(name)

  korean()
  ```

## 클로저

- 중첩 함수에서 `자식함수가 부모함수의 변수를 참조`하고 있고 `부모함수가 자식함수를 return`하는 형태

  ``` python
  def make_name():
      last_name = '아'
      def this_is_name(first_name):
          return last_name + first_name
      return this_is_name

  name = make_name()
  name('이유')  # 아이유
  ```

## 데코레이터
  
- 데코레이터는 함수를 장식한다는 의미로 함수를 wrapping하는 함수를 말한다.
  
  ``` python
  def travel(country):
      def wrapper():
          print(country.__name__ + '행 비행기를 탔습니다.')
          country()
          print(country.__name__ + '에 도착했습니다.')
      return wrapper

  def china():
      print('중국으로 이동합니다.')

  def japan():
      print('일본으로 이동합니다.')

  travel(china)()
  travel(japan)()
  ```

- travel함수는 다른 함수 실행 앞 뒤에 비행기에 타고 내리는 정보를 알려주는 역할을 하는 데코레이터이다.
- 파이썬의 데코레이터는 travel함수와 같이 wrapping한 함수를 return하는 형태로 구현되어야 하며 이렇게 구현된 데코레이터는 다음과 같이 사용 가능하다.

  ``` python
  def travel(country):
      def wrapper():
          print(country.__name__ + '행 비행기를 탔습니다.')
          country()
          print(country.__name__ + '에 도착했습니다.')
      return wrapper

  @travel
  def china():
      print('중국으로 이동합니다.')

  @travel
  def japan():
      print('일본으로 이동합니다.')

  china()
  japan()
  ```

- 다음과 같은 형태로 파라미터와 return을 처리할 수 있다.

  ``` python
  def travel(country):
      def wrapper(city):
          ret = country(city)
          print(country.__name__ + ' ' + city + '행 비행기를 탔습니다.')
          return ret
      return wrapper

  @travel
  def china(city):
      return '중국 ' + city +' 에 입국합니다.'

  @travel
  def japan(city):
      return '일본 ' + city + ' 에 입국합니다.'

  print(china('베이징'))
  print(japan('도쿄'))
  ```

- 클래스도 데코레이터로 만들 수 있으며 그 형태는 다음과 같다.

  ``` python
  class Travel:
      def __init__(self, country):
          print('travel decorator instance 생성 됨')
          self.country = country

      def __call__(self, city):
          print(self.country.__name__ + ' ' + city + '행 비행기를 탔습니다.')
          return self.country(city)

  @travel
  def china(city):
      return '중국 ' + city +' 에 입국합니다.'

  @travel
  def japan(city):
      return '일본 ' + city +' 에 입국합니다.'

  print(china('시안'))
  print(japan('교토'))
  ```