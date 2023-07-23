from flask import Flask,Blueprint,  render_template, url_for, redirect, request
import psycopg2, os
from login import login_bp
from admin import admin_bp
from user import user_bp

app = Flask(__name__)

app.register_blueprint(login_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)

#DB接続
def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

# 最初の画面
@app.route('/')
def index():
    product_list = select_product_list()
    return render_template('index.html' , product_list=product_list)


# 商品検索
@app.route('/search', methods=['POST'])
def search():
    word = request.form.get('word')
    connection = get_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM product WHERE name LIKE %s"
    
    cursor.execute(sql, (word,))
    rows = cursor.fetchall()
    return render_template("search_result.html", rows=rows)


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

if __name__ == "__main__":
    app.run(debug=True)
    