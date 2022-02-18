# DB 관리
import sqlite3
def getconn():
    # db 생성
    conn = sqlite3.connect('./members.db')
    return conn

def create_table():
    # 테이블 생성
    conn = getconn()
    cur = conn.cursor()
    sql = """
        CREATE TABLE member(
            mid char(5) PRIMARY KEY,
            passwd char(8) NOT NULL,
            name text NOT NULL,
            age integer,
            regDate timestamp date DEFAULT (datetime('now','localtime'))
            )
        """
    cur.execute(sql)
    conn.commit()
    print("테이블생성")
    conn.close()

def insert_member():
    # 데이터 입력
    conn = getconn()
    cur = conn.cursor()
    sql = "INSERT INTO member(mid, passwd, name, age) VALUES (?,?,?,?)"
    # cur.execute(sql, ('10001', 'm1234567', '최민정', '24'))
    cur.execute(sql, ('10002', 'm1234568', '안산', '21'))
    cur.execute(sql, ('10003', 'm1234569', '김지은', '30'))
    conn.commit()
    print('회원추가')
    conn.close()

def select_member():
    # 데이터 출력
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member"
    cur.execute(sql)
    rs = cur.fetchall()
    for i in rs:
        print(i)
    conn.close()

# conn = getconn()
# print("접속", conn)
# create_table()
# insert_member()
# select_member()
