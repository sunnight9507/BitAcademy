def define_set():
    """
    셋 자료형 정의 연습
    # 순서가 없다 -> 인덱싱 불가, 슬라이싱 불가
    # 중복이 없음
    # 길이를 측정 Len, 포함 여부 (in, not in)확인 가능
    """

    empty = set() # 빈 셋
    print(empty, type(empty))

    # empty2 = {} # 빈 셋을 만들고자 할 경우는 {} 쓰면 안된다 -> dict
    # print(empty2, type(empty2))

    s = {1,2,3,4,5,6}
    # 길이와 포함 여부는 확인할 수 있다.
    print(s, "LENGTH : ", len(s))
    print(2 in s, 5 not in s)

    # 타 순차 자료형을 기반으로 셋 만들기
    s = "Python Programming"
    chars = set(s.upper()) # 문자열 s -> 셋으로 변경
    print("char set : ", chars)

    # 집합의 특성상 데이터의 중복 제거에 유용
    words = "Python Programming Java Programming HTML Coding".upper().split()
    print("WORDS : ", words)
    # 셋으로 변환
    filtered = set(words)
    print("총 {}개의 단어가 사용되었습니다.".format(len(filtered)))

def set_methods():
    """
    셋의 메서드
    """
    s1 = {1, 3, 5, 7, 9}
    print("SET : ", s1)

    # 셋에 데이터 추가 : add
    s1.add(4) # 셋에 객체 4 추가
    print("ADD : ", s1)
    s1.add(4) # 이미 있는 개체 4 추가
    print("ADD 2nd : ", s1) # 셋은 중복 허용하지 않음

    # 객체의 삭제
    # discard : 객체를 삭제, 없어도 에러 없음
    # remove : 객체를 삭제, 없으면 Error
    s1.discard(4)
    print("DISCARD : ", s1)
    s1.discard(4) # 없는 객체의 삭제
    print("DISCARD 2 : ", s1)

    if 4 in s1:
        s1.remove(4) # 없는 객체의 remove -> Error

    # 셋 내부 데이터의 갱신 : update
    print("SET : ", s1)
    s1.update({2,4,6,8,10})
    print("UPDATE : ", s1)

def set_oper():
    """
    셋은 집합을 다루는 자료형
    합집합 : |, union 메서드
    교집합 : &, interscction 메서드
    차집합 : -, difference

    판별 메서드
        issuperset : 모집합 판별(bool)
        issubset : 부분집합 판별(bool)
    """
    evens = {0,2,4,6,8,10} # 짝수 집합
    odds = {1,3,5,7,9} # 홀수 집합
    numbers = {0,1,2,3,4,5,6,7,8,9,10} # 전체 집합
    mthree = {0,3,6,9} # 3의 배수 집합

    # 합집합
    print("짝수 홀수 합집합 :", evens.union(odds) == numbers)
    print("짝수 홀수 합집합 :", evens | odds == numbers)

    # 모집합, 부분집합 판별
    print("evens는 numbers의 부분집합?", evens.issubset(numbers))
    print("numbers는 odds의 모집합?", numbers.issuperset(odds))

    # 교집합 &, intersection
    print(odds.intersection(mthree) == {3, 9})
    print(evens & mthree == {0,6}) # 짝수 집합과 3의 배수 집합의 교집합

    # 차집합 -, difference
    print(numbers - evens == odds) # 전체 집합에서 짝수 집합을 빼면 홀수
    print(numbers.difference(odds) == evens)

def loop():
    """
    셋의 반복
    # 순서가 없으므로 어떤 순서로 출력될지는 알 수 없다.
    """
    numbers = {1,2,3,4,5,6,7,8,9,10}
    for num in numbers:
        print(num)


if __name__ == "__main__":
    # define_set()
    # set_methods()
    # set_oper()
    loop()