# 함수의 인수
# 필요한 개수만큼 선언할 수 있다
# 어떤 객체든 전달할 수 있다
#   함수도 객체이므로 다른 함수의 인수로 전달할 수 있다

def sum_val(a,b):
    return a + b # 함수 실행 결과를 반환할 경우 return으로 전달

print("sum_val : ", sum_val(10, 20))

def incr(a, step=1): # a를 step만큼 증가시키는 함수
     # step의 기본값은 1, 호출시 step을 명시하지 않으면 기본값 1 사용
    return a + step

print("incr : ", incr(10,2))
print("incr (기본값 사용) :", incr(10))

# 키워드 인수
# 값을 전달할 때 선언되어 있는 인수의 이름을 명시할 수 있다
# -> 선언부에 선언된 순서와 일치하지 않아도 된다
def area(width, height):
    return width * height

print("AREA : ", area(10, 20)) # 함수에 선언된 인수의 순서대로
print("AREA : ", area(width=10, height=20)) # 키워드 인수 사용
print("AREA : ", area(height=20, width=10)) # 키워드 인수는 순서가 달라도 된다

# 가변 인수
# 정해지지 않은 갯수의 인수를 전달 받을 때 사용
# 인수명 앞에 *를 붙여서 선언
def get_total(*nums):
    # 만약 nums 내부의 요소가 int, float 형이면 합산
    # 그 이외의 자료형이면 합산하지 않음
    # print("가변 인수 :", nums)
    total = 0
    for num in nums:
        if isinstance(num, (int, float)):
            total += num
    return total

print(get_total(1,3,5,7,9))
print(get_total(2,4,6))
print(get_total(2,4,"6",8,10)) # "6"은 합산되지 않을 것임

# 사전 키워드 인수
# 정의되지 않은 키워드를 인수로 받을 경우
def func_args(a, b, *c, **kwd):
    print(a,b) # 고정 인수
    print(c, type(c)) # 가변 인수
    print(kwd, type(kwd)) # 사전 키워드 인수

func_args(10, 20, 30, 40, 50, option1 = "value1", option2 = "value2")

# 함수도 객체이므로 다른 함수의 인수로 넘겨줄 수 있다
def add(a,b):
    return a + b

def substract(a, b):
    return a - b

def calc(a, b, func):
    # func는 외부에서 함수를 전달
    if callable(func): # 전달발은 func가 함수인가?
        return func(a,b)

print("calc + add :", calc(10, 20, add)) # 함수의 이름 명시
print("calc + substract :", calc(10, 20, substract))

# 예제
# 정제되지 않은 문자열이 있다
words = "python pRogRammIng, jaVa pRoFRAMMINg, LINUX, WinDOWs".split(",")
print("DIRTY Stringss : ", words)
# words 내부의 문자열들에 문자열 함수를 전달해주어서 정제하는 함수 작성
def clean_strings(strings, *funcs):
    result = [] # 빈 리스트
    for string in strings:
        # 함수의 목록을 루프
        for func in funcs:
            if callable(func): # 가변 인수로 넘어온 func가 함수이면 호출
                string = func(string)
        result.append(string)

    return result

print("CLEANED : ", clean_strings(words, str.strip, str.title))


# 람다 함수
# 익명 함수, 일회성 함수
def square(x):
    return x ** 2

for i in range(1, 11): # 1 ~ 10 까지 Loop를 돌면서 square 함수 수행
    print("{}:{} ".format(i, square(i)), end= " ")
else:
    print()

# 중복 활용해야 할 필요 없이 즉석에서 사용하는 함수
# 위의 것과 동일한 lambda를 활용한 코드 작성
for i in range(1, 11):
    print("{}:{} ".format(i, (lambda x : x**2)(i)), end= " ")
else:
    print()

# 주로 데이터 처리, GUI 이벤트 코드 등 콜백함수를 즉석에서 만들어 낼 경우
# Lambda 함수를 활용

# Lambda 함수의 활용 -> sort, sorted에서 정렬 기준이 되는
# key 함수를 즉석에서 정의할 때 편리
words = "Life is too short, you need Python".upper().replace(",","").split()

print("words : ", words)

# 기본적인 sort
print("sorted asc words : ", sorted(words))
# 역순 정렬 : reverse = True
print("sorted desc words : ", sorted(words, reverse=True))

# 정렬 기준을 문자열의 길이
print("sorted asc length word : ", sorted(words, key=lambda s:len(s)))

# 수치 데이터가 있을 경우
nums = [1,7,5,13,20,15,3]
print("nums", nums)

# 수치 데이터를 역순 정렬
print("sorted desc nums : ", sorted(nums, reverse=True))
# 연습 : 정렬 기준을 5로 나눈 나머지의 역순으로 변경
print("sorted remains desc nums : ", sorted(nums, key = lambda x : x % 5), reverse = True)

















