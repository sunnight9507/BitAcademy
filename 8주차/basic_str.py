# 문자열
# 시퀀스 자료형, 길이, 연결, 반복, 포함여부
# 인덱스, 슬라이싱
# 변경 불가 자료형 -> 내부자료는 변경할 수 없다.
def define_str():
    print("===== 문자열 생성 연습")
    # 한 줄 문자열 쌍따옴표("), 홑따옴표(')
    s1 = "Hello Python"
    s2 = str(3.1415) # 타 타입을 문자열로 변환

    print(s1, "is", type(s1))
    print(s2, "is", type(s2))

    # 여러 줄 문자열 : """", '''
    s3 = """
    Life is too short,
    You need Python
    """
    print(s3)

    """
    여러 줄 문자열은 여러 줄 주석이 필요한 경우에도 사용함수
    정의부 바로 아래 여러 줄 문자열로 도움말을 작성하면
    help 명령어로 해당 함수의 사용밥을 볼 수 있다.
    docstring이라 한다
    """

def string_oper():
    """
    문자열 연산 연습
    """
    s1 = "First String"
    s2 = "Second String"
    
    # 길이를 측정 : Len
    print(s1, "Length: ", len(s1))
    # 인덱싱을 할 수 있다
    print("INDEXING : ", s2[0],s2[1],s2[2],s2[3]) # 정인덱싱
    print("RINDEXING : ", s2[-6], s2[-5], s2[-4], s2[-4])  # 역인덱싱

    # 불변 자료형이므로 내부 자료를 바꿀 수 없다.
    # s2[0] = "p" # Error

    # 슬라이싱
    # [시작경계:끝경계:간격]
    print(s2[1:4] == "yth")
    print(s2[-5:-2] == "yth") # 역인덱스를 이용한 슬라이싱
    
    print(s2[0:3] == "Pyt")
    print(s2[:3] == s2[0:3]) # 시작경계를 생략하면 처음부터
    print(s2[3:len(s2)] == "hon")
    print(s2[3:] == s2[3:len(s2)]) # 끝 경계를 생략하면 끝까지

    print(s2[:] == "Python") # 전체

    print(s2[::2] == "Pto") # 간격값의 재정의
    print(s2[::-1] == "nohtyP") # 간격값이 음수면 방향이 반대

    # 연결 + : 산술연산자가 아니다
    # print("Python" + 3) # Error
    print("Hello" + " " + "Python") # 연산 기호

    # 반복 * 정수형
    print("Ha" * 5) # 5번 반복

    # 포함 여부 확인 : in, not in
    print("R in in s2? ", "R" in s2)
    print("P in not in s2? ", "P" not in s2)


if __name__ == "__main__":
    define_str()
    string_oper()
