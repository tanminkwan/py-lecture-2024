# 내장 컨테이너 자료형
## 내장 컨테이너 자료형

   자료형   |                    설명                     |       사용 예
   ---------- | ------------------------------------------- | -------------------
   List       | 순서가 있는 임의 객체 집합, mutable         | ['ham, 'spam']
   Tuple      | 순서가 있는 임의 객체 집합, immutable       | ('ham, 'spam')
   dictionary | 순서가 없는 객체 집합, key:value쌍. mutable | {'ham':3, 'spam':5}
   set        | 순서가 없는 객체 집합 . mutable             | {'ham','spam'}

## 리스트 자료형

- **리스트는 Java의 array와 유사한 자료형**

- 리스트 만들기

    ``` python
    color_list = ['black', 448668, 'red', 556757, ['blue', 'green']]  # 리스트 안에는 어떤 자료형도 표현 가능.

    print(type(color_list))

    empty_list = []  # 빈 리스트
    empty_list2 = list()  # 빈 리스트
    ```

- 리스트 연산

    ``` python
    colors1 = ['white', 'yellow', 'brown']
    colors2 = ['pink', 'purple', 'sky']

    colors1 + colors2
    colors1 * 3

    [*empty_list, *colors1, *colors2]  # empty_list + colors1 + color2 와 같다.
    ```

- 리스트 인덱싱과 슬라이싱
  문자열의 인덱싱, 슬라이싱과 동일하다.
  문자열과 다른 점은 인덱싱, 슬라이싱을 통해 수정이 가능하다.

    ``` python
    color_list[0]
    color_list[-1]

    color_list[:3]  # 처음부터 3미만의 항목들
    color_list[::2]  # 처음부터 2칸씩의 항목들

    color_list[0] = 'gray' # color_list[0]가 'gray'로 변경
    color_list[2:4] = ['crimson', 665874] # color_list[2] = 'crimson', color_list[3] = 665874s 로 변경

    print(color_list)
    ```

- 리스트 함수

    ``` python
    del color_list[4:]  # 객체 ['blue', 'green'] 삭제

    len(color_list)  # 리스트의 길이

    'grey' in color_list  # list에 해당 값 포함여부

    all(color_list)  # 모든 값이 True이면 True

    any(color_list)  # 일부 값이 True이면 True

    color_list.append('coral')  # 리스트의 맨 끝에 요소 추가

    color_list.index('crimson')  # 해당 값의 위치 찾기

    color_list.remove('crimson')  # 첫번째로 나오는 해당 값을 삭제

    color_list.insert(1, 'silver')  # 해당 위치에 요소 추가

    color_list.reverse()  # 리스트 뒤집기
    reversed(colors1)  # 내장함수 사용. 리스트에 영향을 주지 않고 list_reverseiterator return

    color_list.pop()  # 리스트의 마지막 요소를 return하고 삭제

    color_list.sort()  # 리스트 정렬. TypeError 발생. 리스트의 자료형이 모두 같아야 한다.

    colors1.sort()  # 리스트 정렬.
    sorted(colors2, reverse = True)  # 내장함수 사용. 리스트에 영향을 주지 않고 list return.
    # reverse = True인 경우 내림차순 정렬. sort() 함수에도 파라미터로 적용 가능.

    empty_list.extend(colors1)  # empty_list + colors1 과 같다.
    ```

- range를 사용해서 리스트 만들기

  - range(시작숫자, 종료숫자, 증감값) 의 형태로 표기하며, 연속된 숫자를 생성한다.

  ``` python
  my_range = range(3, 10)  # 3~9
  print(type(my_range))

  range_list = list(range(3, 10))

  rng_inc_2_list = list(range(0, 10, 2))
  ```

## 튜플 자료형

- **튜플은 리스트와 비슷하지만 immutable이다.**
- 튜플 만들기

  ``` python
  lang_tuple = ('python', 'java', ('perl', 'ruby'), ['JS', 'HTML'], 5)  # 튜플 안에는 어떤 자료형도 표현 가능

  empty_tuple = ()  # 빈 튜플
  empty_tuple2 = tuple()  # 빈 튜플
  ```

- 튜플 연산

  ``` python
  lang1 = ('python', 'java', ('perl', 'ruby'))
  lang2 = (['JS', 'HTML'], 5)

  lang1 + lang2

  lang2 * 3

  (*empty_tuple, *lang1, *lang2)  # empty_tuple + lang1 + lang2 와 같다.
  ```

- 튜플 인덱싱과 슬라이싱
  리스트의 인덱싱, 슬라이싱과 동일하지만 수정할 수 없다.

  ``` python
  lang_tuple[0]

  lang_tuple[-1]

  lang_tuple[:3]  # 처음부터 3미만의 항목들

  lang_tuple[::2]  # 처음부터 2칸씩의 항목들

  lang_tuple[1] = 'C++'  # TypeError 발생. 튜플은 immutable
  ```

- 튜플, 리스트 간 변환하기

  ``` python
  list_from_tuple = list(lang_tuple)

  # 리스트 → 튜플
  tuple_from_list = tuple(list_from_tuple)

  # range → 튜플
  range_tuple = tuple(range(3, 10))
  ```

- 리스트와 튜플로 변수 만들기

  ``` python
  lang1, lang2, lang3 = lang_tuple[:3]
  print(lang1, lang2, lang3, sep=' / ')
  ```

## 딕셔너리 자료형

- **key, value를 한 쌍으로 갖는 자료형. Java의 HashMap과 유사하다.**
- **항목의 순서를 따지지 않으며 key는 imuutable타입만 가능며 중복 불가하다. value는 mutable도 가능.**
- 딕셔너리 만들기

  ``` python
  # tuple도 immutable 자료형이므로 key로 사용 가능하다.
  zoo_dict = {'개':'DOG', '고양이':'CAT', '소':'COW', ('사자', '호랑이'):{'LION','TIGER' }, '새': ['PIGEON','SWALLOW']}

  empty_dict = {}  # 빈 딕셔너리
  empty_dict2 = dict()  # 빈 딕셔너리
  ```

- 딕셔너리의 value접근

  ``` python
  # key를 사용해서 value를 얻어낸다.
  zoo_dict['개']

  # key로 접근해서 value를 수정할 수 있다.
  zoo_dict['개'] = 'PUPPY'

  # 존재하지 않는 key로 assign하면 새로운 쌍을 추가
  zoo_dict['닭'] = 'CHICKEN'

  zoo_dict['말']  # KeyError발생
  zoo_dict.get('말', 'HORSE')  # key가 없으면 뒤의 파라미터를 return
  ```

- 딕셔너리는 key의 중복을 허용하지 않는다.

  ``` python
  my_dict = {1:'one', 1:'first', 2:'two', 2:'second'}
  print(my_dict)  # 중복 된 키가 존재하면 뒤의 것만 남는다. : {1: 'first', 2: 'second'}
  ```

- 딕셔너리 함수

  ``` python
  tmp_dict = {1:10, 2:20, 3:30}

  {**empty_dict, **zoo_dict, **tmp_dict}  # dict 합치기

  len(zoo_dict)  # 딕셔너리 key 개수 구하기

  '개' in zoo_dict  # 해당 키 포함여부

  all(zoo_dict)  # 모든 키 값이 True이면 True

  any(zoo_dict)  # 어떤 키 값이 True이면 True

  zoo_dict.update(토끼='RABBIT')

  zoo_dict.pop('개')  # get과 동일하지만 pop한 쌍을 삭제

  del zoo_dict['닭']  # 해당 key의 쌍 삭제하기

  zoo_dict.popitem()  # 마지막 키-값 쌍을 삭제하고 키-값 쌍을 튜플로 반환

  zoo_dict.keys()  # dict_keys객체 반환.

  zoo_dict.values()  # dict_values객체 반환.

  zoo_dict.items()  # dict_items객체 반환. key, value 쌍이 tuple로 반환됨.
  ```

- 딕셔너리와 문자열 포매팅

  ``` python
  baseball_dict = {'homerun': 467, 'name': '이승엽'}
  '{name}은 전직 야구선수로 KBO 통산 홈런 갯수는 {homerun}개 이다.'.format(**baseball_dict)
  ```

## 집합 자료형

- **집합은 수학의 집합과 동일한 역할을 하는 자료형으로 mutable하다.**
- **집합의 속성은 imuutable해야 한다.**
- **집합의 항목들은 순서가 없으며 중복을 허용하지 않는다. 이런 특징 때문에 자료형의 중복을 제거하기 위한 필터로 종종 사용된다.**

- 집합 만들기

  ``` python
  marvel_set = set(('hulk', 'thanos', 'iron_man', ('thor', 'loki'), 'captain_marvel'))  # set 함수를 이용하여 초기화 할때는 tuple이나 list를 파라미터로 넣는다.

  marvel_set_2 = {'ant_man', ['groot', 'gamora']}  # type error발생. mutable한 list는 set의 속성이 될 수 없다.

  marvel_set_2 = {'ant_man', ('groot', 'gamora'), 'ant_man', 'hulk'}  # 중복을 허용하지 않으므로 ant_man은 하나만 들어간다.

  empty_set = set()
  ```

- 집합 연산자

  ``` python
  marvel_set | marvel_set_2  # 합집합

  marvel_set & marvel_set_2  # 교집합

  marvel_set - marvel_set_2  # 차집합

  marvel_set ^ marvel_set_2  # XOR(합집합에서 교집합 뺀 부분)
  ```

- 집합 함수

  ``` python
  len(marvel_set)  # 집합의 요소의 개수

  set.union(marvel_set, marvel_set_2)  # 합집합

  set.intersection(marvel_set, marvel_set_2)  # 교집합

  set.difference(marvel_set, marvel_set_2)  # 차집합

  set.symmetric_difference(marvel_set, marvel_set_2)  # XOR

  marvel_set.add('captain_america')  # 값 1개 추가

  marvel_set.update(['spider_man', 'black_widow'])  # 값 여러개 추가

  marvel_set.remove('captain_america')  # 해당 값 삭제 값이 없으면 에러

  marvel_set.discard('captain_america')  # 해당 값 삭제 값이 없어도 에러 안남

  marvel_set.pop()  # 임의의 값 반환하고 삭제

  {*marvle_set, *marvel_set_2}  # 집합 합치기
  ```

## 내장 컨테이너 자료형 정리

<table style="border: 1px solid #000000; border-collapse: collapse; border-style: none">
  <thead>
    <th style="border: 1px solid #000000; width: 140;">자료형</th>
    <th style="border: 1px solid #000000; width: 110;">가변성</th>
    <th style="border: 1px solid #000000; width: 70;">유형1</th>
    <th style="border: 1px solid #000000; width: 200;" colspan="2">특징1</th>
    <th style="border: 1px solid #000000; width: 70;">유형2</th>
    <th style="border: 1px solid #000000; width: 200;">특징2</th>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #000000;" align="center">
          String
      </td>
      <td style="border: 1px solid #000000;" rowspan="2">
          immutable
      </td>
      <td style="border: 1px solid #000000;" rowspan="3">시퀀스형</td>
      <td style="border: 1px solid #000000;" rowspan="3" colspan="2">
          index사용
          <br> slicing
          <br> +, * 연산
          <br> min(), max(), index(), count() 함수 사용
      </td>
      <td style="border: 1px solid #000000;" rowspan="5">내장 컨테이너</td>
      <td style="border: 1px solid #000000; width: 100" rowspan="5">
          len() 사용
          <br> in, all(), any() 사용
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #000000;" align="center">
          Tuple
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #000000;" align="center">
          List
      </td>
      <td style="border: 1px solid #000000;" rowspan="3">
          mutable
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #000000;" align="center">
          Dictionary
      </td>
      <td style="border: 1px solid #000000;" align="center">
          사전형
      </td>
      <td style="border: 1px solid #000000; width: 400">
          key로 접근 <br> key, value 관련 함수 사용 (keys(), values(), items())
      </td>
      <td style="border: 1px solid #000000; width: 150" rowspan="2">
          update() 함수 사용
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #000000;" align="center">
          Set
      </td>
      <td style="border: 1px solid #000000;" align="center">
          집합형
      </td>
      <td style="border: 1px solid #000000;">
          집합 함수 사용 (intersection(), union())
      </td>
    </tr>
  </tbody>
</table>