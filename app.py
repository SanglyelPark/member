import sqlite3

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# db 접속 함수
def getconn():
    conn = sqlite3.connect("./members.db")
    return conn
# index
@app.route('/')
def index():
    return render_template('index.html')

# 회원 목록
@app.route('/memberlist/')
def memberlist():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member ORDER BY regDate DESC"
    cur.execute(sql)
    rs = cur.fetchall()
    conn.close()
    return render_template('memberlist.html', rs=rs)

# 회원 상세 페이지
@app.route('/member_view/<string:id>/')
def member_view(id):
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM member WHERE mid = '%s'" % (id)
    cur.execute(sql)
    rs = cur.fetchone()   # 회원 한명을 전송
    conn.close()
    return render_template('member_view.html', rs=rs)

# 회원 가입
@app.route('/register/', methods= ['GET','POST'])
def register():
    if request.method == "POST":
        # 데이터 가져오기
        id = request.form['mid']
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']

        conn = getconn()
        cur = conn.cursor()
        sql = "INSERT INTO member(mid, passwd, name, age) " \
               "VALUES ('%s','%s','%s','%s')" % (id, pwd, name, age)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect(url_for('memberlist'))
    else:
        return render_template('register.html')

# 로그인 페이지
@app.route('/login/')
def login():
    return render_template('login.html')
app.run(debug=True)