def func():
    # 블록은 들여쓰기가 시작되는곳에서 시작된다.
    pass  # 블록은 비어있으면 안됨. 구현부가 없을 경우에는 pass


def func2():
    print("hello", "python", sep=",", end="!\n")


def arith_oper():
    print("===산술연산자")
    print("7/5 ?", 7 / 5)
    print("7/5 의 몫", 7 // 5)
    print("7/5 의 나머지", 7 % 5)
    # divmod()
    print("divmod(7,5)", divmod(7, 5))
    print("divmod(7,5)의 몫", divmod(7, 5)[0])
    print("divmod(7,5)의 나머지", divmod(7, 5)[1])
    print("2의 3승", 2 ** 3)
    print("pow(2,3)", pow(2, 3))


def rel_oper():
    print("====비교 연산")
    print("1>3?", 1 > 3)
    print("6==9?", 6 == 9)
    print("6!=9?", 6 != 9)

    a = 6
    print(a, "가 0~10사이?", 0 < a < 10)
    print(a, "가 0~10사이?", 0 < a and a < 10)

    print("문자열 비교", "abd" < "abc")
    print("리스트 비교", [1, 2, 3] < [1, 2, 4])
    print("튜플 비교", (1, 2, 3) < (1, 2, 4))


def variable_ex():
    print("====== 변수의 할당")
    import keyword
    print("예약어 목록 =", keyword.kwlist)
    가격 = 10000
    a = 10
    b, c = 20, 30
    print(b, c)

    d = e = f = 40
    print(d, e, f)

    g = 2020
    print("g", g, type(g))
    g = "python"
    print("g", g, type(g))

    if isinstance(g, str):
        print(g, "는 문자열")
    else:
        print(g, "는 문자열이 아님")

    h = 2020
    if isinstance(h, (int, float, complex)):
        print(h, "는 산술연산가능")
    else:
        print(h, "는 산술연산불가")


if __name__ == "__main__":
    func()
    func2()
    arith_oper()
    rel_oper()
    variable_ex()

