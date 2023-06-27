from flask import Blueprint, render_template, request
import hashlib, string, random, psycopg2, os

login_bp = Blueprint('login', __name__, url_prefix='/login')


def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits
    salt = '' .join(random.choices(charset, k=30))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 200).hex()
    return hashed_password


# アカウント登録遷移
@login_bp.route('/regist')
def regist():
    return render_template('regist/regist.html')

#アカウント登録情報入力
@login_bp.route('/regist_conf', methods=['POST'])
def regist_conf():
    name = request.form.get('name')
    mail = request.form.get('mail')
    password = request.form.get('password')
    salt = get_salt()
    hashed_password = get_hash(password, salt)
    sql = 'INSERT INTO users(username, mail, salt, password) VALUES(%s, %s, %s, %s)' #id, name, mail, hashedpassword, salt
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        print(name, mail, hashed_password )
        
        cursor.execute(sql, (name, mail, salt, hashed_password))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally :
        cursor.close()
        connection.close()
        print(count)
    return render_template('regist/regist_execute.html', name=name, mail=mail, hashed_password=hashed_password)


#ログイン 
@login_bp.route('/login')
def login(pw,  mail):
    return render_template('login/login.html')