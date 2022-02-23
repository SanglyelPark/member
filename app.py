import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from tbl_member import select_member


app = Flask(__name__)

app.secret_key = "#abcde!"

# db 접속 함수
def getconn():
    conn = sqlite3.connect("./members.db")
    return conn

# index 페이지
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
@app.route('/member_view/<string:id>/', methods = ['GET'])
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

        # 저장(회원 가입)
        conn = getconn()
        cur = conn.cursor()
        sql = "INSERT INTO member(mid, passwd, name, age) " \
               "VALUES ('%s','%s','%s','%s')" % (id, pwd, name, age)
        cur.execute(sql)
        conn.commit()
        #자동 로그인
        sql = "SELECT * FROM member WHERE mid = '%s' AND passwd = '%s'" % (id, pwd)
        cur.execute(sql)
        rs = cur.fetchone()
        if rs:
            session['userID'] = rs[0]   # 회원 가입시 세션 발급
            return redirect(url_for('memberlist'))
        conn.close()
        return redirect(url_for('memberlist'))  #redirect 페이지 이동
    else:
        return render_template('register.html')

# 로그인 페이지
@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        # 입력된 id 비번을 가져오기
        id = request.form['mid']
        pwd = request.form['passwd']

        # db 연동
        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s' AND passwd = '%s'" % (id, pwd)
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()
        if rs:
            session['userID'] = rs[0]
            return redirect(url_for('index'))
        else:
            error = "아이디나 비밀번호를 확인해주세요"
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/logout/')
def logout():
    session.pop("userID")  #세션 삭제
    return redirect(url_for('index'))

# 회원 삭제
@app.route('/member_del/<string:id>/')
def member_del(id):
    conn = getconn()
    cur = conn.cursor()
    sql = "DELETE FROM member WHERE mid = '%s'" % (id)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return redirect(url_for('memberlist'))

@app.route('/member_edit/<string:id>/', methods=['GET','POST'])
def member_edit(id):
    if request.method == 'POST':
        # 데이터 가져오기
        mid = request.form['mid']
        pwd = request.form['passwd']
        name = request.form['name']
        age = request.form['age']

        # db 연동
        conn = getconn()
        cur = conn.cursor()
        sql = "UPDATE member SET passwd='%s', name='%s', age='%s' " \
                "WHERE mid = '%s'" % (pwd, name, age, mid)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect(url_for('member_view', id=id))  #해당 경로 아이디
    else:
        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM member WHERE mid = '%s'" % (id)  #해당 경로 아이디
        cur.execute(sql)
        rs = cur.fetchone()   #수정할 회원정보
        conn.close()
        return render_template('member_edit.html', rs=rs)

# 게시글 목록
@app.route('/boardlist/')
def boardlist():
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board ORDER BY bno DESC"
    cur.execute(sql)
    rs = cur.fetchall()
    conn.close()
    return render_template('boardlist.html', rs=rs)

#게시글 상세 페이지
@app.route('/board_view/<int:bno>/')
def board_view(bno):
    conn = getconn()
    cur = conn.cursor()
    sql = "SELECT * FROM board WHERE bno = '%s'" % (bno)
    cur.execute(sql)
    rs = cur.fetchone()
    conn.close()
    return render_template('board_view.html', rs=rs)

# 게시글쓰기
@app.route('/writing/', methods = ['GET', 'POST'])
def writing():
    if request.method == "POST":
        # 데이터를 넘겨 받음
        title = request.form['title']
        content = request.form['content']
        mid = session.get('userID') # 로그인한 mid(글쓴이)

        conn = getconn()
        cur = conn.cursor()
        sql = "INSERT INTO board(title, content, mid) " \
                "VALUES ('%s', '%s', '%s')" % (title, content, mid)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect(url_for('boardlist'))
    else:
        return render_template('writing.html')

@app.route('/board_del/<int:bno>')
def board_del(bno):
    conn = getconn()
    cur = conn.cursor()
    sql = "DELETE FROM board WHERE bno = '%s'" % (bno)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return redirect(url_for('boardlist'))

# 게시글 수정
@app.route('/board_edit/<int:bno>/', methods = ['GET','POST'])
def board_edit(bno):
    if request.method == "POST":
        # 데이터 ㅈ너달 받기
        title = request.form['title']
        content = request.form['content']
        mid = session.get('userID')

        # db 연동
        conn = getconn()
        cur = conn.cursor()
        sql = "UPDATE board SET title='%s', content='%s', mid='%s' " \
              "WHERE bno = '%s'" % (title, content, mid, bno)
        cur.execute(sql)
        conn.commit()
        conn.close()
        return redirect(url_for('board_view', bno=bno))  # 해당 경로 아이디
    else:
        conn = getconn()
        cur = conn.cursor()
        sql = "SELECT * FROM board WHERE bno = '%s'" % (bno)
        cur.execute(sql)
        rs = cur.fetchone()
        conn.close()
        return render_template('board_edit.html', rs=rs)


app.run(debug=True)