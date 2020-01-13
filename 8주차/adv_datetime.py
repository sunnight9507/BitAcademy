# datatime 모듈
# date 객쳬 : 연월일
# time 객체 : 시분초마이크로초, 요일 정보
# datatime 객체 : date 객체, + time 객체
# timedelta : 두 datetime 객체의 시간 차이를 다루는 객체
import datetime # 모듈 불러오기

def get_datetime():
    # 시간의 획득 : 현재시간
    now = datetime.datetime.now()
    print("현재 날짜 : ", now)

    # 객체 함수를 이용해 지정된 날짜 정보 생성
    dt = datetime.datetime(1999, 12, 31) # 최소한 년월일 정보는 지정해야 한다
    print("날짜 정보 : ", dt)

    # dt2 = datetime.datetime(1999, 12, 32) # 없는 날짜의 생성 -> Error

    # datetime 객체의 주요 속성과 메서드
    print("now : ", now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond)
    print("오늘 무슨 요일? ", now.weekday()) # 요일 반환 메서드 0 : 월 ~ 6 : 일

    now_dt = now.date() # 년월일 등 날짜 관련 데이터 담은 date 객체 반환
    now_tm = now.time() # 시분초 등 시간 관련 데이터 담은 time 객체 반환

    print("now date : ", now_dt)
    print("date의 속성들 : ", now_dt.year, now_dt.month, now_dt.day, now_dt.weekday())
    print("now time : ", now_tm)
    print("time의 속성들 : ", now_tm.hour, now_tm.minute, now_tm.second, now_tm.microsecond)

def timedelta_ex():
    # 두 datetime은 대소 비교할 수 있고
    # 차이를 얻어낼 수 있다 : 두 날짜의 차이 -> timedelta
    now = datetime.datetime.now() # 현재 날짜와 시간
    print("NOW : ", now)
    past = datetime.datetime(1999, 12, 31) # 과거의 날짜
    print("PAST : ", past)

    # 대소 비교
    print("NOW > PAST : ", now > past)

    delta = now - past # 두 datetime의 차이 -> timedelta
    print("DELTA : ", delta, type(delta))

    # timedelta의 주요 속성과 메서드들
    print("timedelta의 속성 : ", delta.days, delta.seconds, delta.microseconds)

    # datetime + timedelta -> 새로운 datetime
    # 현재 날짜와 시간으로부터 365일이 지난 날짜와 시간은?
    diff = datetime.timedelta(days = 365, seconds = 0, microseconds=0)
    print("365일이 지난 후의 시간 : ", now + diff)

def format_date():
    # strftime : datatime -> 포맷 -> str
    # strptime : str -> 포맷 -> datatime

    # strftime
    now = datetime.datetime.now()

    # now(datetime) -> 0000-00-00 00:00:00
    print("STRFTIME : ", now.strftime("%Y-%m-%d %H-%M-%S"))
    # now(datetime) -> 0000년 00월 00일 00시 00분 00초

    # 한글 Encoding 문제 해결 방법
    import locale
    locale.setlocale(locale.LC_ALL, "ko_KR.UTF-8")

    print("STRFTIME : ", now.strftime("%Y년 %m월 %d일 %H시 %M분 %S초"))

    # strptime : datetime 모듈의 함수
    s = "2020-01-13 15:40:15"
    dt = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S") # s문자열 -> 포맷
    print("STRPTIME : ", dt, type(dt))

    # 만약 문자열과 날짜 포맷이 다르면 -> 에러
    # dt2 = datetime.datetime.strptime(s, "%Y년 %m월 %d일") # ValueError


if __name__ == "__main__":
    # get_datetime()
    # timedelta_ex()
    format_date()