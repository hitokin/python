from flask import Blueprint, render_template, request
import hashlib, string, random, psycopg2, os

login_bp = Blueprint('login', __name__, url_prefix='/login')

#DB接続
def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

#ソルト取得
def get_salt():
    charset = string.ascii_letters + string.digits
    salt = '' .join(random.choices(charset, k=30))
    return salt

#ハッシュ取得
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


#ログイン処理
def login_process():
    sql = 'SELECT * FROM users WHERE mail = %s AND password = %s'
    mail = request.form.get('mail')
    password = request.form.get('password')
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (mail, password))
        user = cursor.fetchone()
             
    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()
        print(type(user))
    return flg


#パスワード取得
def get_account_pass(mail):
    sql = 'SELECT password FROM users WHERE mail = %s'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (mail,))
        passw = cursor.fetchone()
        str_pw = str(passw[0])
        
        
    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()
        
    return str_pw

#ソルト取得
def get_account_salt(mail):
    sql = 'SELECT salt FROM users WHERE mail = %s'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (mail,))
        salt = cursor.fetchone()
        str_salt = str(salt[0])
        
        
    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()
        
    return str_salt

#ログイン 
@login_bp.route('/login')
def login():
    return render_template('login/login.html')

#入力後の画面遷移
@login_bp.route('/login_exe', methods=['POST'])
def login_exe():
    mail = request.form.get('mail')
    password = request.form.get('password')
    print('入力パスワード' + password)
    #データベースからソルト取得
    salt = get_account_salt(mail)
    hashed_password = get_hash(password, salt)
    
    #データベースからパスワードとソルト取得
    passw = get_account_pass(mail)
    if mail == "admin@mail" and hashed_password == passw :
        return render_template('admin_home.html', passw=passw, error="成功") 
    elif  hashed_password == passw :
        #成功でホーム画面
        product_list = select_product_list()
        return render_template('home.html', passw=passw, error='成功', product_list=product_list)
    else :
        return render_template('login/login.html', passw=passw, error='失敗')
    
@login_bp.route('/home')
def move_home():
    return render_template('admin_home.html')

@login_bp.route('/index', methods=['POST'])
def move_index():
    return render_template('login/login.html')

#ログアウト確認
@login_bp.route('/logout_conf')
def logout_conf():
    return render_template('login/logout_conf.html')

#ログアウト
@login_bp.route('/logout')
def logout():
    return render_template('index.html')


#商品表示
def select_product_list():
    sql = "SELECT * FROM product WHERE stack != 0"

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    product_list = cursor.fetchall()
    cursor.close()
    connection.close()
    print(product_list)
    print(type(product_list))

    return product_list