# 함수 / lambda / 클래스

## 함수

- 함수 기본구조

  ```python
  def 함수명(매개변수):
      statement
  ```

- 함수 결과값 리턴하기

  ```python
  # 한 개의 반환값
  def area(a):
      return a ** 2
  # 두 개의 반환값
  def area2(a):
      area = a ** 2
      volume = a ** 3
      return (area, volume)
  ```

- 가변인자
  - `*`(Positional) : '*' 를 매개변수 앞에 붙이면 정해지지 않은 수의 인자를 받는다는 의미 (튜플 형태)

    ```python
    # 기본구조
    def 함수명(*args_tuple):
        statement

    def words(*args):
        print(type(args))
        for i in args:
            print(i)

    words('사과','포도','바나나')
    ```

  - `**`(Keyword) : '**' 를 매개변수 앞에 붙이면 정해지지 않은 수의 키워드 인자를 받는다는 의미 (딕셔너리 형태)

    ```python
    # 기본구조
    def 함수명(**args_dict):
        statement

    def words(**kargs):
        for key, value in kargs.items():
            print(f'{key} 는 {value}')

    words(a='사과', b='포도',c='바나나')
    ```

- docstring(documentation strings)
  함수에 대한 설명을 정의할 수 있음.

  ```python
  def 함수명(매개변수):
      """독스트링설명"""
      statement
  ```

  ```python
  def area(a):
      """ 주어진 길이에 대한 넓이를
      계산합니다 """
      return a ** 2
  help(area)
  ```

- default 파라미터
  함수의 매개변수에 default 파라미터를 지정할 수 있으며, 기본값 지정시 매개변수 생략이 가능하다.

  ```python
  def area3(a, h = 4):
      area = a ** 2
      volume = a ** h
      return (area, volume)
  area3(2)
  ```

## lambda

- 익명함수로 함수를 한 줄로 간결하게 만들 때 사용하며 메모리를 절약하는 이점이 있음
- lambda 기본구조

  ```python
  lambda 매개변수 : statement
  # if 문을 사용할 경우 반드시 else 문을 사용해야 한다
  lambda 매개변수 : statement1 if 조건문 else statement2
  ```

  ```python
  # 일반함수
  def square(x,y):
      return x * y

  # 람다함수
  lambda x, y : x * y
  lambda x, y : x * y if x == 2 else x + y
  ```

- 매개변수로 함수를 사용할 때 주로 사용한다.

  ```python
  def test_func (f, arg):
    return f(arg)

  test_func(lambda x : x**2, 3)
  ```

- lambda 와 map의 활용
  - map 함수란? : map 은 매개변수로 '함수'와 반복가능한(iterable) 객체를 받아, 객체의 각 요소에 함수가 적용된 결과를 리턴
    (map은 원본 리스트를 변경하지 않고 새 리스트를 형성)

    ```python
    list(map(함수, 리스트))
    tuple(map(함수, 튜플))
    ```

    ```python
    # map예제 : 각 요소에 함수를 적용한 새로운 리스트를 생성하는 경우
    nums = [1, 2, 3, 4, 5]

    def calc(x):
        return x**2

    double_nums = []
    for x in nums:
        double_nums.append(calc(x))   
    print(double_nums)

    # map 
    print(list(map(calc, nums)))
    ```

    ```python
    # lambda 와 map 을 활용
    nums = [1, 2, 3, 4, 5]
    print(list(map(lambda x : x**2, nums)))
    ```

## 클래스

- class 라는 예약어를 사용하여 class 임을 명시.
- class 기본구조

  ```python
  # 클래스 생성
  class Bread:
      def __init__(self):
          self.shape = "붕어"
          self.source = "팥앙금"

      def intro(self):
          return f'{self.source} 이 들어간 {self.shape}빵이에요!!'
  # Bread 클래스 인스턴스(객체) 생성
  fish = Bread()
  ```

- `__init__(self)` function
  - 인스턴스를 생성할 때 자동으로 먼저 `__new__` 를 호출하여 객체를 생성하고 `__new__` 메소드가 `__init__` 메소드를 호출하여 인스턴스에서 사용할 변수 초기화(initialize)한다. 
    일반적으로 파이썬에서 클래스를 만들 시 `__init__` 메소드를 오버라이딩하여 객체초기화에 이용한다.
  - self 는 자기자신을 가리키며, 암묵적으로 첫 인자로 인스턴스 객체가 전달된다.
  - 일반적으로 변수 초기화 및 객체 생성시 들어오는 값에 대하여 validation 을 수행

  ```python
  class Bread:
      def __init__(self, scoup):
          if scoup <= 0:
              raise ValueError("0보다 커야 합니다.")
          self.scoup = scoup

  a  = Bread(0)
  ```

- 클래스 변수와 인스턴스 변수
  - 클래스 변수 : 클래스 내부에 선언된 변수
  - 인스턴스 변수 : self 가 붙어 있는 변수
  ```python
  # 클래스 생성
  class Bread:
      # 클래스 변수 class variable shared by all instances
      num = 0
      special = "카스타드"
      def __init__(self, shape, source):
          # 인스턴스 변수 instance variable unique to each instance
          self.shape = shape
          self.source = source
          Bread.num += 1

      # 인스턴스 메소드
      def intro(self):
          return f'{self.source} 이 들어간 {self.shape}빵이에요!!'

  fish = Bread("붕어", "팥앙금")
  flower = Bread("국화", "크림")
  ```

- 클래스 상속(Inheritance)
  - 부모 클래스의 속성을 그대로 자식 클래스에서 받아서 쓸 수 있음.
  - 자식 클래스의 선언부에 상속받을 부모 클래스 리스트를 괄호 안에 명시한다.

  ```python
  class ChildBread(Bread):
      pass # 클래스나 함수에서 아무것도 안 할 경우 pass 로 명시  

  child = ChildBread("붕어", "팥앙금")
  child.intro()
  ```

- 클래스메소드와 스태틱 메소드
  - 클래스 메소드
    - @classmethod 데코레이터 사용
    - 클래스변수에 접근 가능
    - 첫번째 인자로 클래스 자체(cls)를 넣어줘야 합니다.

    ```python
    @classmethod
    def commons(cls):
        return f'총 구워진 빵은 {cls.num}개이고 특별하게 {cls.special}도 들어갑니다.'

    Bread.commons()
    ```

  - 스태틱 메소드
    - @staticmethod 데코레이터 사용
    - 객체를 따로 선언할 필요없이 함수를 호출 할 수 있음
    - 인스턴스(self)나 클래스(cls)를 인자로 받지 않음
    ```python
    @staticmethod
    def bake(time = '50'):
        return f'빵을 {time}초씩 앞뒤로 구워보아요.'
    # override
    print(Bread.bake('40'))
    ```

    - 상속시 @classmethod 를 활용하면 부모클래스의 속성이 아니라,
      현재 클래스 속성을 사용할 수 있다.

      ```python
      class ChildBread(Bread):
          special = "아기별모양"

      ChildBread.commons()
      ```

- 메소드 오버라이딩(overriding, 덮어쓰기)
  - 메소드 오버라이딩이란? : 부모 클래스에 있는 메서드를 동일한 이름으로 다시 만드는 것

    ```python
    class Test:
        def __init__(self):
            self.a = "John"

        def greet(self):
            print("Hello!! " + self.a)

    class ChildTest(Test):
        def greet(self):
            print("Hi every one!!")

    hey = ChildTest()
    hey.greet()
    ```

  - **super()** 라는 키워드를 사용하여 자식 클래스에서도 부모클래스를 호출 할 수 있다.

    ```python
    class ChildTest2(Test):
        def greet(self):
            super().greet()
            print("Hi every one!!")
    ```

  - 파이썬은 메소드 오버로딩이 없다.
    - 메소드 오버로딩이란? : 하나의 클래스 내부에서 메소드 명칭은 똑같고, 인자를 다르게 하는 형태
    - java 는 아래와 같은 코드를 허용

    ```java
    // java
    class Test{
      static String greet(String a){
        return "Hello! " + a
      }
      static String greet(String a, String b){
        return "Hello! " + a + ", " + b
      }
    }
    ```

    ```python
    # python
    class Test:
        def __init__(self, a):
            self.a = "John"

        def greet(self):
            print("Hello !!" + self.a)

        def greet(self, b):
            print("Hello !!" + self.a + "," + b)

    hey = Test("Tom")
    hey.greet()
    ```