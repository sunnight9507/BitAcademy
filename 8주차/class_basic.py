# class
# class는 멤버(데이터), 메서드(함수) 한 이름 공간 안에 작성한 것
# class는 새로운 데이터 자료형의 설계도
# class를 실제 객체로 만드는 작업을 인스턴스화,
#   만들어진 실제 객체는 인스턴스

# 클래스의 정의
class MyString(str):
    pass
    # 부모 클래스로 str을 확장하여 만듦
    # MyString은 str로부터 모든 멤버와 메서드를 물려 받는다

print("----- MyString ")
s = MyString("새로 만든 MyString 클래스")
print("MyString : ", s)
s = MyString("Python Object Oriented Programming")
print("MyString : ", s)
# MyString은 str을 확장했기 때문에, str이 가진 모든 기능을 그대로 사용
print("s.lower : ", s.lower())

# type 확인
print("s is ", type(s))
print("s class : ", s.__class__) # 어떤 클래스인지 확인

# 부모 클래스의 확인
print("s의 부모는 ? ", MyString.__bases__) # 부모 클래스의 확인
print("s는 MyString의 인스턴스인가?", isinstance(s, MyString))
print("s는 str의 인스턴스인가?", isinstance(s, str))










