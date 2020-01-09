# 튜플
# 리스트와 거의 비슷하지만 불변 자료형
# 순서가 있고 -> 인덱싱, 슬라이싱
# 불변 자료 -> 슬라이싱 활용 삽입, 치환, 삭제 불가
# 연결(+), 반복(*), 포함 여부 확인(in, not in)

def define_tuple():
    """
    튜플 정의 연습
    """
    t = tuple() # 공튜플
    t = tuple({1,2,3}) # 타 순차 자료형을 튜플로 캐스팅
    print(t, type(t))

    t2 = (1,2,3) # 튜플 기호를 이용한 생성
    t3 = () # 공튜플
    print(t2, t3)

    t4 = (1,) # 항목이 한 개인 경우 반드시 콤마
    print(t4, type(t4))
    
def tuple_oper():
    """
    튜플의 연산
    """
    tp = (1,2,3,4,5)
    # 길이를 가진 순서가 있는 자료형
    print(tp, "LENGTH : ", len(tp))

    # 인덱싱이 가능
    print(tp[0], tp[1], tp[2]) # 정인덱싱
    print(tp[-5], tp[-4], tp[-3]) # 역인덱싱
    
    # 슬라이싱, 연결, 반복 모두 가능
    # 불변자료형, 내부 데이터의 변경, 슬라이싱을 이용한 삽입, 치환, 삭제 불가
    print("3 in tp", 3 in tp)
    
def assignment():
    """
    튜플의 할당
    """
    # 기본적으로는 ()로 묶어줘야 하지만 없어도 튜플로 인식
    t = (10,20,30)
    t2 = 10,20,30 # ()가 없어도 튜플
    print(t, type(t))
    print(t2, type(t2))

    print(t2, "LENGTH:", len(t2)) # 내부 요소가 3개
    x, y, z = t2 # 우변 튜플을 각 요소를 좌변의 변수에 각각 대입
    print(x,y,z)

def packing_unpacking():
    """
    패킹과 언패킹
    """
    tp = (10,20,30, "Python")
    print(tp, type(tp))
    tp = 10,20,30,"Python" # 튜플 기호 없이도 튜플로 인식 -> 위 문장과 동일
    print(tp, type(tp))

    # 기본 Unpacking : 우변의 튜플 각 요소를 좌변의 변수 객체에 할당
    a,b,c,d = tp
    print("Basic Unpacking : ",a,b,c,d)

    # a,b,c = tp # 좌변 변수 갯수가 부족 -> Error
    # a,b,c,d,e = tp # 우변 값의 갯수가 부족 -> Error

    # 요소 갯수에 상관 없이 할당할 경우 -> 할당 언패킹 *
    a, *b = tp # tp로부터 1개 요소를 a에 할당, 나머지는 확장 언패킹 변수에 할당
    print(a,b)
    *a, b = tp # tp로부터 마지막 1개 요소를 b에 할당, 나머지는 확장 언패킹 변수에 할당
    print(a,b)
    a, *b, c = tp
    print(a,b,c)
    
def tuple_methods():
    """
    튜플의 메서드
    # 리스트와 거의 동일, 불변 자료형
    """
    tp = 20, 30, 10, 20
    print("Count of 20 : ", tp.count(20))

    print("Index of 20 : ", tp.index(20))


if __name__ == "__main__":
    # define_tuple()
    # tuple_oper()
    # assignment()
    # packing_unpacking()
    tuple_methods()