# 함수의 스코핑(영역) 룰
x = 1

def scope_func(a):
    print("LOCAL : ", locals())
    print("x in global?", "x" in locals())
    print("x in globals?", "x" in globals())
    return a + x # x는 local 스코프에 없으므로 global x를 활용

print(scope_func(10))

def scope_func2(a):
    x = 2 # x의 할당 작업이 일어났으므로
    # 로컬 스코프에 x가 생겼을 것
    print("\nx in locals?", "x" in locals())

    return a + x
    # 함수 내부에서 x의 할당 작업이 일어났으므로, 로컬 영역에 x가 생성

print(scope_func2(10))

def scope_func3(a):
    global x # 지금부터 x는 글로벌 변수임을 명시
    x = 3
    print("\nx in locals? ", "x" in locals())
    print("x in globals?", "x" in globals())
    return a + x

print("scope_func3 : ", scope_func3(10))
# scope_func 내부에서 global x를 변경
print("global x : ", x)

# 네임 스페이스의 확인
# Locals 함수 -> 로컬 영역의 네임 스페이스 확인
# globals 함수 -> 글로벌 영역의 네임 스페이스 확인
# dir 함수 -> 글로벌 영역, 혹은 builtin 영역의 네임스페이스 확인
print("DIR : ", dir())
print("builtin 영역 : ", dir('__builtins__')) # builtin 영역 네임스페이스 확인















