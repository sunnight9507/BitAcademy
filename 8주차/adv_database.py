# DBAPI : 데이터 베이스에 접속하기 위한 python의 표준 API
# sqlite
import sqlite3
from sqlite3 import Error

dbfile = "./database/mysqlite.db" # 데이터 베이스 파일

def create_connection():
    # 데이터 베이스 저장을 위한 디렉터리
    import os # 운영체제 기능 수행을 위한 모듈
    if os.path.exists("./database"):
        # database 디렉토리가 없으면 생성
        os.makedirs("./database")

    # Connection
    try:
        conn = sqlite3.connect(dbfile)
        print(sqlite3.version)
    except Error as e:
        print("접속 오류:", e, type(e))

    return conn

def test_create_table():
    conn = create_connection() # 데이터베이스 접속
    cursor = conn.cursor()
    # DDL(Create Table)
    ddl = """
    CREATE TABLE IF NOT EXISTS
    customer(
        id INTEGER PRIMARY KEY
        name VARCHAR(20),
        category INTEGER,
        region VARCHAR(10)
    )
    """
    
    cursor.execute(ddl)
    conn.close() # 꼭 닫아주자

def test_insert_data(name, category, region):
    conn = create_connection()
    cursor = conn.cursor()

    # # 익명 파라미터 바인딩 : ? -> 데이터는 튜플로
    # sql = """
    # INSERT INTO customer (name, category, region)
    # VALUES (?,?,?)
    # """
    #
    # res = conn.execute(sql, (name, category, region))

    # 명명된 파라미터 바인딩 : :파라미터명 -> 데이터는 dict
    sql = """
    INSERT INTO customer (name, category, region)
    VALUES (:name, :category, :region)
    """

    res = conn.execute(sql, {"name" : name,
                             "category" : category,
                             "region" : region})

    print("{}개의 레코드가 영향을 받음".format(res.rowcount))
    # Transaction : commit or rollback
    conn.commit() # 데이터 변경을 실제 데이터 베이스에 반영
    conn.close()

def test_delete_all():
    conn = create_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM customer"
    res = cursor.execute(sql)

    print("{}개의 레코드가 삭제!".format(res.rowcount))
    conn.commit()
    conn.close()
    
def insert_bulk_data():
    test_delete_all()
    test_insert_data("둘리", 1, "부천")
    test_insert_data("고길동", 2, "상계동")
    test_insert_data("마이콜", 2, "상계동")
    test_insert_data("홍길동", 3, "한양")
    test_insert_data("임꺽정", 3, "안양")

def test_select_data():
    conn = create_connection()
    sql = """
    SELECT * FROM customer
    """

    cursor = conn.execute(sql)

    # 레코드 받아오기
    # fetchone -> 1개 레코드 받아오기
    print("fetchone")
    print(cursor.fetchone())
    print("fetchmany") # 여러 개 받아오기
    print(cursor.fetchmany(2)) # 커서의 위치에서 2개의 레코드
    print("fetchall") # 모든 레코드
    print(cursor.fetchall())

def test_search_data():
    conn = create_connection()
    # 익명 Place Holder : ? -> 데이터는 튜플
    sql = """
    SELECT * FROM customer
    WHERE region = ?
    """
    cursor = conn.execute(sql, ("상게동",))

    # 루프
    for customer in cursor.fetchall():
        print("상계동 주민 : ", customer)

    # category 필드가 3인 고객 명단을
    # 명명된 파라미터 방식으로
    sql = """
    SELECT * FROM customer
    WHERE category=:cat
    """

    cursor = conn.execute(sql, {"cat" : 3})
    print("카테고리 3의 고객 : ")
    for customer in cursor.fetchall():
        print(customer)

    conn.close()



if __name__ == "__main__":
    # test_create_table()
    # test_insert_data("둘리", 1, "부산")
    # test_delete_all()
    # insert_bulk_data()
    test_select_data()