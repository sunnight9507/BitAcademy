def bool_ex():
    print(bool(0),bool(10))
    print("true는 bool?",isinstance(True,bool))
    print("true는 int?", isinstance(True, int))

    a=5
    print(a, 0<a<10)
    print(a, a>0 and a<10)
    print(a, a<=0 or a>=10)

    print(bool(0),bool(2020))
    print(bool(""), bool("python"))
    print(bool([]), bool([1,2,3]))

# 정수형(int)
def int_ex():
    print("===== 정수형 연습")
    a = 2020
    b = int("2020") # 타 데이터 타입을 정수형으로 변환(캐스팅)
    print(a, type(a))
    print(b, type(b))

    # 2진, 8진, 16진 정수 표기
    b = 0b1010
    o = 0o23
    x = 0xFF
    print(b, o , x)

    # Python 3.x Long, int 형을 구분하지 않음
    # Long 데이터 타입 8byte를 초과하는 정수도 처리
    i = 123456789012345679123456789012345679
    print(i)
    print("i의 비트 수:", i.bit_length())

    # 진법 변환 함수 : 정수형을 진법 변환 -> str
    print("42 -> 2진수 :", bin(42))
    print("42 -> 8진수 :", oct(42))
    print("42 -> 16진수 :", hex(42))

def float_ex():
    print("===== 실수형 연습")
    # 소숫점을 표함하거나 지수 표기법으로 된 실수 데이터
    a = 3.1451
    b = float("3.1415") # 타 데이터 타입을 실수형으로 캐스팅

    print(a, "is", type(a))

    c = 3.0
    # 형태 판별 : is_integer()
    print(a, "is", type(a))
    print(a, "는 정수 형태?", a.is_integer()) # 형태 판별, 타입 판별이 아님
    print(c, "is", type(c))
    print(c, "는 정수 형태?", c.is_integer())

def complex_ex():
    print("===== 복소수 연습")
    # 실수부 + 허수부
    # 산술 연산 가능
    a = 4 +5J
    print(a, "is", type(a))
    # 실수부와 허수부가 따로 있을 때
    b = complex(7,-2) # 복소수 생성
    print(b, "is", type(b))

    # 산술 연산
    print(a + b)
    # 실수부와 허수부 확인
    print(a, "의 실수부 : ", a.real)
    print(a, "의 허수부 : ", a.imag)

def internal_math():
    print("===== 내장 수치 함수")
    
    print(abs(-3)) # 절댓값
    print(divmod(5,3)) # 나눗셈이 몫과 나머지
    print("5를 3으로 나눈 몫:", divmod(5,3)[0])
    print("5를 3으로 나눈 나머지:", divmod(5, 3)[1])

if __name__=="__main__":
    # bool_ex()
    # int_ex()
    # float_ex()
    # complex_ex()
    internal_math()