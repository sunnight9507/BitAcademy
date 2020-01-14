# point.Point 클래스 테스트
from point import Point

def test_bound_instance_method():
    # 인스턴스에 직접 접근하여 내부의 메서드를 수행
    p = Point()
    p.set_x(10)
    p.set_y(20)
    print("p -> x : {}, y : {}".format(p.get_x(), p.get_y()))

def test_unbound_method():
    # 클래스를 통한 우회접근으로 메서드를 수행
    # 어떤 객체의 메서드인지 식별하기 위해 실제 인스턴스를 전달
    p = Point()
    Point.set_x(p, 10)
    Point.set_y(p, 20)

    print("Unbound : p -> x : {}, y : {}".format(Point.get_x(p), Point.get_y(p)))

def test_lifecycle():
    p1 = Point()
    p1.set_x(10)
    p1.set_y(20)

    print("Point의 객체 수 : ", Point.count_of_instance)
    print("p1 : ", p1)

    p2 = Point()
    p2.set_x(30)
    p2.set_y(40)

    print("Point의 객체 수 : ", Point.count_of_instance)
    print("p2 : ", p2)

    del p1
    print("Point의 객체 수 : ", Point.count_of_instance)
    del p2
    print("Point의 객체 수 : ", Point.count_of_instance)

def test_repr():
    # repr 함수에 객체를 넘기면 객체 내부의 __repr__이 수행
    p = Point(x = 30, y = 40)

    print("__str__ : ", p)
    print("__repr__ : ", repr(p))

    # __repr__ 메서드를 출력된 문자열로 다시 객체를 복원할 수 있어야 한다
    p2 = eval(repr(p))

    print("복원된 객체 : ", p2)
    print("p == p2 ?", p == p2)

def test_oper_overloading():
    """
    연산자 오버로딩
    """
    print("Point + Point :", Point(10,10) + Point(20, 20))
    print("Point + int :", Point(10, 10), 20)

    # class Point 내에 __add__를 오버로딩 했따 -> 연산 수행
    
    print("int + Point : ", 20 + Point(10, 10))
    # 기본적인 연산자 수행 실패했을 경우, 뒤쪽  클래스가
    # 다시 한번 점검 할 수 있다. -> 역이행 연산자

    p1 = Point(10, 10)
    # eval : 문자열을 코드로 실행시켜주는 함수
    p2 = eval(repr(p1))

    print("p1 : ", p1)
    print("p2 : ", p2)
    print("p1 == p2? ", p1 == p2) # __eq__ 오버로딩

from point import ColorPoint

def extend_ex():
    """
    상속된 클래스의 생성과 사용
    """
    cp = ColorPoint(10, 20, "RED")
    # ColorPoint는 Point가 가진 모든 멤버와 메서드를 상속 받았다
    print("cp:", cp)

if __name__ == "__main__":
    # test_bound_instance_method()
    # test_unbound_method()
    # test_lifecycle()
    # test_repr()
    # test_oper_overloading()
    extend_ex()