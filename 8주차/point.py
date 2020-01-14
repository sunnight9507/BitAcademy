class Point:
    # Point는 부모를 명시하지 않았지만 가장 상위 클래스인 object를 확장한 것
    count_of_instance = 0 # 클래스 멤버
    # 클래스 멤버는 모든 인스턴스에서 공유할 수 있는 멤버

    # 객체의 생명 주기 : Lifecycle
    def __init__(self, x = 0, y = 0): # 생성자
        # 파이썬의 생성자는 여러 형태로 만들 수 없기 때문에
        # 인수와 기본값을 활용하여 여러 형태에 대응하는 
        # 단 하나의 생성자를 만든다
        print("Point 생성자 호출")
        # 초기화 수행
        self.x, self.y = x, y
        Point.count_of_instance += 1 # 클래스 멤버에 접근

    def __del__(self): # 소멸자
        print("Point 소멸자 호출")
        Point.count_of_instance -= 1 # 클래스 멤버에 접근

    def __enter__(self):
        # with ~ as 키워드와 함께 사용했을 때 호출
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # with ~ as 블록이 종료될 때 호출
        # -> 자원의 정리 작업 수행
        pass

    def __str__(self):
        # print 혹은 str 함수에 넘겨줬을 때 출력 포맷을 지정하는 메서드
        # 기본 출력 포맷은 클래스명 at 메모리 주소
        return "Point x={} y={}".format(self.x, self.y)

    def __repr__(self):
        # repr 함수에 넘겨주었을 때 반환되는 문자열
        # 이 문자열을 활용, 객체를 복원가능해야 한다.
        return "Point({}, {})".format(self.x, self.y)

    # 인스턴스 메서드
    #   첫번째 인자는 반드시 self여야 한다
    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    # 연산자 오버로딩
    # 새 클래스의 생성은 새로운 데이터 타입 생성
    # -> 해당 데이터 타입에 대한 연산 행동을 지정해 줄 필요가 있다
    def __add__(self, other): # + 연산자의 오버로딩
        # Point + Point ->
        # Point + int ->
        if isinstance(other, Point): # Point + Point의 연산
            return Point(self.x + other.x, self.y + other.y)
        if isinstance(other, int): # Point + int의 연산
            return Point(self.x + other, self.y + other)
        # 나머지 -> 어떻게 하지
        return self + other

    def __radd__(self, other): # + 연산자의 역이행 오버로딩
        # other는 + 연산자 앞쪽의 객체
        if isinstance(other, int):
            return Point(self.x + other, self.y + other)
        # 그 이외의 경우
        return other + self

    def __eq__(self, other): # == 연산자의 오버로딩
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return self == other

    @classmethod
    def class_method(cls): # cls는 해당 클래스의 참조
        # 클래스 영역 내부에서는 개별 인스턴스 영역의 멤버와 메서드는 접근할 수 없다.
        print("class method call")

    @staticmethod
    def static_method():
        # 클래스 영역에도, 개별 인스턴스 영역에도 접근할 수 없다.
        # 특정 클래스의 이름 공간에 포함된 함수일 뿐
        print("static method call")

# 상속
# Point를 확장 -> ColorPoint를 생성
# x, y, color 세가지 멤버를 가지는 새로운 클래스
class ColorPoint(Point):
    # ColorPoint는 Point 클래스의 모든 멤버와 메서드를 상속 받는다
    def __init__(self, x = 0, y = 0, color="black"):
        # x, y는 이미 Point 클래스에 초기화 코드가 있다
        # 부모인 Point의 생성자를 먼저 호출
        super().__init__(x, y)
        self.color = color # 추가 정의 멤버

    def __str__(self):
        return "ColorPoint x={}, y={}, color={}".format(self.x, self.y, self.color)












