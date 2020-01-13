# 파일 모드
# 파일의 타입에 대한 구분 : test(t - default), binary(b),
# 파일을 다루는 액션에 대한 구분 : read(r - default), write(w), append(a)

def write_test01():
    # 파일 열기
    f = open("./sample/test.txt",  # 파일명
                "wt", # 파일모드 - write text
                encoding="UTF8" # 인코딩
    )

    # 파일에 내용 기록
    size = f.write("Life is too short, you need Python")
    print(size, "만큼 기록!")

    # 중요 : 파일을 open했으면 반드시 close 해준다.
    f.close()

def read_test01():
    # 텍스트 파일을 읽어와서 출력
    f = open("./sample/test.txt", "rt", encoding="UTF8")
    # 텍스트 파일 읽기 모드
    data = f.read()
    print("파일 내용 : ", data)
    f.close()

def write_multiline():
    # 여러 라인을 텍스트 파일로 저장
    f = open("./sample/multilines.txt", "wt", encoding="UTF8")

    for i in range(1, 11):
        f.write("Line {}\n".format(i))
    f.close() # 반드시 닫아 주자

def read_multilines():
    # 여러 라인 텍스트를 읽어오기
    f = open("./sample/multilines.txt", "rt", encoding="UTF8")
    data = f.read()
    print("data : ", data)
    # 한번에 데이터를 불러올 경우,
    #   파일 사이즈가 클 경우 메모리 문제가 발생할 가능성이 있다.

    lines = data.split("\n") # 개행 문자를 기준으로 분리 -> 리스트

    for index, line in enumerate(lines):
        print("{}번째 라인 : {}".format(index, line))

    f.close()

def read_multiline02():
    # 파일 객체의 readLine 메서드를 사용하면 줄단위로 텍스트를 읽을 수 있다.
    f = open("./sample/multilines.txt", "rt", encoding="UTF8")

    lines = []
    # 몇 줄의 텍스트가 있는지 모르기 때문에 무한 루프
    while True: # 무한 루프
        print("현재 파일 포인터의 위치 : {}".format(f.tell()))
        line = f.readline()

        # 더 이상 읽을 내용이 없을 경우 ""
        if len(line) == 0:
            break
        else:
            lines.append(line.strip())

    print("LINES : ", lines)
    f.close()

def read_multiline03():
    # 편의 메서드 : readline
    # 전체 데이터를 불러와서 -> 개행 문자 기준으로 split -> 리스트로 만들기
    f = open("./sample/multilines.txt", "rt", encoding="UTF8")
    lines = f.readlines()

    # 각 요소에 있는 개행 문자를 지운다
    lines = [line.strip() for line in lines]
    print("LINES : ", lines)
    f.close()

def handle_binary():
    # rose-flower.jpeg를 rose-flower-copy.jpeg로 복제
    # binary 파일은 b로 명시
    f_src = open("./sample/rose-flower.jpeg", "rb") # binary 파일임을 명시

    # 바이너리 데이터 읽기
    data = f_src.read()
    f_src.close()

    # 복제 대상 파일 열기
    f_dest = open("./sample/rose-flower-copy.jpeg", "wb")

    # 바이너리 데이터 저장
    f_dest.write(data)
    f_dest.close()

    print("파일 복제 완료!")

def with_as():
    # 파일, DBMS, 네트워크 등 시스템 자원은 open하고 사용을 했으면
    # 반드시 닫아줘야 한다.
    # with ~ as 문을 사용하면 자동으로 자원을 close
    with open("./sample/multilines.txt", "rt", encoding="UTF8") as f:
        print("내용 : ", f.read())
        # close는 안해도 된다

# Pickle 모듈
# 파이썬 객체 -> 바이트 스트림 형태로 적절화
# 바이트 스트림 파일 -> 파이썬 객체로 역직렬화 해주는 모듈
import pickle # pickle 모듈을 사용하려면 import

def pickle_dump():
     # pickle은 바이트 스트림 형태로 직렬화하므로 파일 모드는 반드시 b 모드
     with open("./sample/players.bin", "wb") as f:
         lst = [1,2,3,4,5]
         dct = {"baseball": 9}
         dct2 = {"soccer": 11}

         # 객체 직렬화
         pickle.dump(lst, f)
         # 원래 단일 객체 직렬화 용이지만,
         # dump 여러번 하면 복수 개의 객체를 직렬화 할 수 있다.
         pickle.dump(dct, f)
         pickle.dump(dct2, f, pickle.HIGHEST_PROTOCOL)
         # dump시 프로토콜 버전을 명시할 수 있다.


def pickle_load():
    # 역직렬화
    with open("./sample/players.bin", "rb") as f:
        # dump시 프로토콜 버전을 명시했더라도
        # Load시에는 명시하지 않느다 -> 파일에 버전이 저장
        """
        print(pickle_load(f))
        print(pickle_load(f))
        print(pickle_load(f))
        """
        # 파일 내부에 직렬화된 피클 객체의 수보다
        # 많은 객체를 역직렬화 하고자 하면 -> EOFError

        # Pickle 객체를 저장할 리스트
        data_list = []

        while True:
            try:
                data = pickle.load(f)
            except EOFError:
                break # 더 이상 역직렬화 할 객체가 없음
            data_list.append(data)

        for obj in data_list:
            print("피클 객체 : ", obj, type(obj))


if __name__ == "__main__":
    # write_test01()
    # read_test01()
    # write_multiline()
    # read_multilines()
    # read_multiline02()
    # read_multiline03()
    # handle_binary()
    # with_as()
    pickle_dump()
    pickle_load()