from flask import Flask, render_template, url_for, redirect, request
import psycopg2
from login import login_bp
app = Flask(__name__)

app.register_blueprint(login_bp)

# 最初の画面
@app.route('/')
def index():
    return render_template('index.html')

# 商品検索
@app.route('/search')
def search():
    connection = psycopg2.connect(user='postgres',
                                password='morijyobi',
                                host='localhost',
                                database='postgres')
    cursor = connection.cursor()

    sql = "SELECT * FROM foods WHERE name LIKE %s"
    key = '%' + key + '%'
    cursor.execute(sql, (key,))

    rows = cursor.fetchall()
    
    result = []
    return render_template()

if __name__ == "__main__":
    app.run(debug=True)
