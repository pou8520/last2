from flask import Flask, render_template, request, session,jsonify
import pymysql

# import hashlib

app = Flask(__name__)

# db = pymysql.connect(host='127.0.0.1',
#                      port=3306,
#                      user='root',
#                      passwd='qwe[]!23',
#                      db='2_project',
#                      charset='utf8')

db = pymysql.connect(host='secendproj.cczokkdg0lti.ap-northeast-1.rds.amazonaws.com', port=3306, user='admin',
                     passwd='roqkfwkehlrhtlqwh', db='2_project', charset='utf8')
cursor = db.cursor()

app.secret_key = 'your secret key'


@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/signup')
def signup_page():
    return render_template('signup.html')


@app.route('/main')
def main_page():
    return render_template('index.html')


@app.route('/none1')
def none1_page():
    return render_template('none1.html')


@app.route('/none2')
def none2_page():
    return render_template('none2.html')


@app.route('/none3')
def none3_page():
    return render_template('none3.html')


@app.route('/none4')
def none4_page():
    return render_template('none4.html')


# 로그인 기능


@app.route('/', methods=['GET', 'POST'])
def login_btn():
    db = pymysql.connect(host='secendproj.cczokkdg0lti.ap-northeast-1.rds.amazonaws.com', port=3306, user='admin',
                         passwd='roqkfwkehlrhtlqwh', db='2_project', charset='utf8')
    cursor = db.cursor()

    msg = ''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        username = request.form['username']
        password = request.form['password']

        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s AND pw = %s', (username, password))

        account = cursor.fetchone()
        print(account)

        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            msg = '로그인 성공'
            return render_template('/index.html', msg=msg)
        else:
            msg = '로그인 실패!'
    return render_template('login.html', msg=msg)

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


## 창민님 .py

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

# POST 구현


@app.route("/save_comment", methods=["POST"])
def comment_post():
    db = pymysql.connect(host='secendproj.cczokkdg0lti.ap-northeast-1.rds.amazonaws.com',
                         port=3306,
                         user='admin',
                         passwd='roqkfwkehlrhtlqwh',
                         db='2_project',
                         charset='utf8')
    cursor = db.cursor()

    name_receive = request.form['name_give']
    comment_receive = request.form['comment_give']
    sql = f'''INSERT INTO pagination(name, comment)
            VALUES('{name_receive}', '{comment_receive}');'''
    cursor.execute(sql)

    db.commit()
    db.close()
    return jsonify({'msg': '게시글 전송 완료!'})

# DELETE 구현


@app.route("/delete", methods=["DELETE"])
def comment_delete():
    db = pymysql.connect(host='secendproj.cczokkdg0lti.ap-northeast-1.rds.amazonaws.com',
                         port=3306,
                         user='admin',
                         passwd='roqkfwkehlrhtlqwh',
                         db='2_project',
                         charset='utf8')
    cursor = db.cursor()

    id_receive = request.form['id']
    sql = f'''DELETE FROM pagination
            WHERE id = {id_receive};'''
    cursor.execute(sql)

    db.commit()
    db.close()
    return jsonify({'msg': '게시글 삭제!'})

# PUT 구현


@app.route("/put", methods=["PUT"])
def comment_put():
    db = pymysql.connect(host='secendproj.cczokkdg0lti.ap-northeast-1.rds.amazonaws.com',
                         port=3306,
                         user='admin',
                         passwd='roqkfwkehlrhtlqwh',
                         db='2_project',
                         charset='utf8')
    cursor = db.cursor()

    id_receive = request.form['id']
    correction_receive = request.form['correction_give']
    sql = f'''UPDATE pagination
            SET comment = '{correction_receive}'
            WHERE id = {id_receive};'''
    cursor.execute(sql)

    db.commit()
    db.close()
    return jsonify({'msg': '게시글 수정 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
