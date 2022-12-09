from flask import Flask, render_template, request, session
from flask import redirect, send_file, url_for, jsonify  # 김재광 추가
from werkzeug.utils import secure_filename
from datetime import timedelta  # 세션 유효기간을 설정하기 위함.
import pymysql
import os

import json

# import hashlib

app = Flask(__name__)
app.secret_key = 'your secret key'
app.permanent_session_lifetime = timedelta(minutes=10)
# 세션의 유효기간 10분
# session.permanent는 기본적으로 false
# 로그아웃 없이 브라우저를 닫아도 세션이 더 저장되어 로그인 상태유지

# db = pymysql.connect(host='127.0.0.1',
#                      port=3306,
#                      user='root',
#                      passwd='qwe[]!23',
#                      db='2_project',
#                      charset='utf8')

db = pymysql.connect(host='secendproj.cczokkdg0lti.ap-northeast-1.rds.amazonaws.com', port=3306, user='admin',
                     passwd='roqkfwkehlrhtlqwh', db='2_project', charset='utf8')
cursor = db.cursor()


@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/signup')
def signup_page():
    return render_template('signup.html')


@app.route('/main')
def main_page():
    if "username" in session:
        username = session["username"]  # 로그인을 했다면(세션안에 정보가 있으니) 로그인하여 생성된 세션 딕셔너리의 값을 변수 username에 저장
        return render_template('index.html',
                               username=username)  # 저장된 username 변수를 main.html 페이지로 전달, 즉 유저마다 각기다른 /user페이지를 보게됨
    else:  # 세션이 존재하지 않는 경우
        return redirect(url_for("login_btn"))  # 세션안에 정보가 없어서(혹은 브라우저를 나가면 세션이 삭제) 로그인 페이지로 redirect


# 회원정보(회원 프로필)
@app.route('/profile')
def my_profile():
    if "username" in session:
        username = session["username"]  # 로그인을 했다면(세션안에 정보가 있으니) 로그인하여 생성된 세션 딕셔너리의 값을 변수 username에 저장
        nickname = session["nickname"]
        email = session["email"]
        password = session["password"]
        return render_template('profile.html',
                               username=username,nickname=nickname,email=email,password=password)  # 저장된 username 변수를 profile.html 페이지로 전달, 즉 유저마다 각기다른 /user페이지를 보게됨
    else:  # 세션이 존재하지 않는 경우
        return redirect(url_for("login_btn"))  # 세션안에 정보가 없어서(혹은 브라우저를 나가면 세션이 삭제) 로그인 페이지로 redirect


@app.route('/edit_profile', methods=['PUT'])
def edit_profile():
    cursor = db.cursor()

    userid = session['id']
    nickname_receive = request.form['nickname_give']
    email_receive = request.form['email_give']
    password_receive = request.form['password_give']
    sql = f'''UPDATE accounts
                    SET nickname = '{nickname_receive}',email = '{email_receive}',pw = '{password_receive}'
                    WHERE id = {userid};'''
    cursor.execute(sql)

    db.commit()
    db.close()
    session['nickname'] = nickname_receive
    session['email'] = email_receive
    session['password'] = password_receive

    return jsonify({'msg': '회원정보 수정 완료!'})


@app.route("/delete_account", methods=["DELETE"])
def delete_account():
    userid = session['id']
    sql = f'''DELETE FROM accounts
            WHERE id = {userid};'''
    cursor.execute(sql)
    db.commit()
    db.close()

    session.pop('username', None)
    return jsonify({'msg': '회원탈퇴 완료!'})


@app.route('/none1')
def none1_page():
    if "username" in session:
        username = session["username"]  # 로그인을 했다면(세션안에 정보가 있으니) 로그인하여 생성된 세션 딕셔너리의 값을 변수 username에 저장
        return render_template('none1.html',
                               username=username)  # 저장된 username 변수를 main.html 페이지로 전달, 즉 유저마다 각기다른 /user페이지를 보게됨
    else:  # 세션이 존재하지 않는 경우
        return redirect(url_for("login_btn"))  # 세션안에 정보가 없어서(혹은 브라우저를 나가면 세션이 삭제) 로그인 페이지로 redirect


@app.route('/none2')
def none2_page():
    if "username" in session:
        username = session["username"]  # 로그인을 했다면(세션안에 정보가 있으니) 로그인하여 생성된 세션 딕셔너리의 값을 변수 username에 저장
        return render_template('none2.html',
                               username=username)  # 저장된 username 변수를 main.html 페이지로 전달, 즉 유저마다 각기다른 /user페이지를 보게됨
    else:  # 세션이 존재하지 않는 경우
        return redirect(url_for("login_btn"))  # 세션안에 정보가 없어서(혹은 브라우저를 나가면 세션이 삭제) 로그인 페이지로 redirect


# @app.route('/none3')
# def none3_page():
#     return render_template('none3.html')


# @app.route('/none4')
# def none4_page():
#     return render_template('none4.html')


# 로그인 기능

@app.route('/', methods=['GET', 'POST'])
def login_btn():
    db = pymysql.connect(host='secendproj.cczokkdg0lti.ap-northeast-1.rds.amazonaws.com', port=3306, user='admin',
                         passwd='roqkfwkehlrhtlqwh', db='2_project', charset='utf8')
    cursor = db.cursor()

    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        username = request.form['username']
        password = request.form['password']  # 해당 form에 입력받은 값을 각각 변수로 선언

        cursor.execute(  # SQL 문을 실행
            'SELECT * FROM accounts WHERE username = %s AND pw = %s', (username, password))

        account = cursor.fetchone()
        print(account)

        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            session['nickname'] = account[2]
            session['email'] = account[3]
            session['password'] = account[4]
            msg = '로그인 성공'
            session.permanent = True  # 세션 작동
            return render_template('/index.html', msg=msg)
        else:
            msg = '로그인 실패!'
        db.close()
    return render_template('login.html', msg=msg)


# 로그아웃기능
@app.route("/logout")
def logout():
    session.pop("username", None)  # 로그아웃하면 세션 정보가 삭제
    return redirect(url_for("login_btn"))  # login_btn 함수가 있는 url페이지로 리디렉션을 반환


# 회원가입 기능
@app.route("/signup", methods=["POST"])
def signup_btn_click():
    db = pymysql.connect(host='secendproj.cczokkdg0lti.ap-northeast-1.rds.amazonaws.com', port=3306, user='admin',
                         passwd='roqkfwkehlrhtlqwh', db='2_project', charset='utf8')
    cursor = db.cursor()

    name_receive = request.form['name_give']
    nickname_receive = request.form['nickname_give']
    email_receive = request.form['email_give']
    password_receive = request.form['password_give']

    sql = f'''INSERT INTO accounts(username, nickname, email, pw)
        VALUES('{name_receive}','{nickname_receive}','{email_receive}','{password_receive}');'''
    cursor.execute(sql)
    db.commit()
    return jsonify({'msg': '회원가입 완료!'})


### 게시글 작성###
# 페이지 네이션
@app.route("/comment/<int:page_id>", methods=["GET"])
def comment_get(page_id):
    db = pymysql.connect(host='secendproj.cczokkdg0lti.ap-northeast-1.rds.amazonaws.com',
                         port=3306,
                         user='admin',
                         passwd='roqkfwkehlrhtlqwh',
                         db='2_project',
                         charset='utf8')
    cursor = db.cursor()

    if page_id == 1:
        sql = '''SELECT * FROM pagination
              LIMIT 10 OFFSET 0;'''
    if page_id == 2:
        sql = '''SELECT * FROM pagination
              LIMIT 10 OFFSET 10;'''
    if page_id == 3:
        sql = '''SELECT * FROM pagination
              LIMIT 10 OFFSET 20;'''
    if page_id == 4:
        sql = '''SELECT * FROM pagination
              LIMIT 10 OFFSET 30;'''
    if page_id == 5:
        sql = '''SELECT * FROM pagination
              LIMIT 10 OFFSET 40;'''

    cursor.execute(sql)
    data_list = cursor.fetchall()

    db.close()
    return jsonify({'data_list': data_list})


# 게시글 작성
@app.route("/save_comment", methods=["POST"])
def comment_post():
    db = pymysql.connect(host='secendproj.cczokkdg0lti.ap-northeast-1.rds.amazonaws.com',
                         port=3306,
                         user='admin',
                         passwd='roqkfwkehlrhtlqwh',
                         db='2_project',
                         charset='utf8')
    cursor = db.cursor()

    if "username" in session:
        username = session["username"]
        id = session['id']
        name_receive = username
        comment_receive = request.form['comment_give']
        id_receive = id
        sql = f'''INSERT INTO pagination(name, comment, secret)
                VALUES('{name_receive}', '{comment_receive}', '{id_receive}');'''
        cursor.execute(sql)
    else:
        return redirect(url_for("login_btn"))  # login_btn 함수가 있는 url페이지로 리디렉션을 반환

    db.commit()
    db.close()
    return jsonify({'msg': '게시글 전송 완료!'})


# 게시글 삭제
@app.route("/delete", methods=["DELETE"])
def comment_delete():
    db = pymysql.connect(host='secendproj.cczokkdg0lti.ap-northeast-1.rds.amazonaws.com',
                         port=3306,
                         user='admin',
                         passwd='roqkfwkehlrhtlqwh',
                         db='2_project',
                         charset='utf8')
    cursor = db.cursor()

    if "username" in session:  # 로그인 후, 세션안에 유저네임 이 있으면
        aaa = session["id"]  # 해당 유저의 아이디에 따라 생성된 값을 변수에 저장하고
        id_receive = request.form['id']  # 선택한 게시글의 db를 조회하고
        sql = f'''SELECT secret FROM pagination WHERE id = {id_receive}'''
        cursor.execute(sql)
        a = cursor.fetchone()

        if str(aaa) == str(a[0]):  # 게시글에 같이 저장된 (pagination 테이블의) secret 컬럼 값이 동일하면
            id_receive = request.form['id']  # 해당 게시글 삭제가 되는 다음 구문을 실행합니다.
            sql = f'''DELETE FROM pagination
                                WHERE id = {id_receive};'''
            cursor.execute(sql)
        else:
            return jsonify({'msg': '타인의 글은 삭제할 수 없습니다.'})

    db.commit()
    db.close()
    return jsonify({'msg': '게시글 삭제!'})


# 게시글 수정
@app.route("/put", methods=["PUT"])
def comment_put():
    db = pymysql.connect(host='secendproj.cczokkdg0lti.ap-northeast-1.rds.amazonaws.com',
                         port=3306,
                         user='admin',
                         passwd='roqkfwkehlrhtlqwh',
                         db='2_project',
                         charset='utf8')
    cursor = db.cursor()

    if "username" in session:  # 로그인 후, 세션안에 유저네임 이 있으면
        aaa = session["id"]  # 해당 유저의 아이디에 따라 생성된 값을 변수에 저장하고
        id_receive = request.form['id']  # 선택한 게시글의 db를 조회하고
        sql = f'''SELECT secret FROM pagination WHERE id = {id_receive}'''
        cursor.execute(sql)
        a = cursor.fetchone()

        if str(aaa) == str(a[0]):  # 게시글에 같이 저장된 (pagination 테이블의) secret 컬럼 값이 동일하면 해당 게시글 삭제가 되는 다음 구문을 실행합니다.
            id_receive = request.form['id']
            correction_receive = request.form['correction_give']
            sql = f'''UPDATE pagination
                    SET comment = '{correction_receive}'
                    WHERE id = {id_receive};'''
            cursor.execute(sql)
            db.commit()
            db.close()
            return jsonify({'msg': '게시글 수정 완료!'})
        else:
            return jsonify({'msg': '타인의 글은 수정할 수 없습니다.'})
    return redirect(url_for("none1_page"))


# 파일업로드 HTML
@app.route('/upload')
def render_file():
    return render_template('upload.html')


# 업로드 처리시
@app.route('/fileUpload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        upload_files = request.files['file']
        # 저장할 경로 + 파일명
        upload_files.save('./static/uploads/' + secure_filename(upload_files.filename))
        files = os.listdir("./static/uploads/")  # static 폴더 아래 uploads 폴더 형성해야함
    return render_template('check.html')


# 다운로드 HTML
@app.route('/downfile')
def down_page():
    files = os.listdir("./static/uploads")
    return render_template('download.html', files=files)


# 파일 다운로드
@app.route('/download', methods=['GET', 'POST'])
def download_file():
    files_list = os.listdir("./static/uploads")  # static 폴더 아래 uploads 폴더 형성해야함
    if request.method == 'POST':
        sw = 0
        for x in files_list:
            if (x == request.form['file']):
                sw = 1
        try:
            path = "./static/uploads/"
            return send_file(path + request.form['file'],
                             download_name=request.form['file'],
                             as_attachment=True,
                             )
        except:
            print("download error")
    return render_template('download.html', files=files_list)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
