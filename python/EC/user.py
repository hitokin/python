from flask import Flask, Blueprint, render_template, request
import psycopg2, os
user_bp = Blueprint('user', __name__, url_prefix='/user')

#DB接続
def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

#商品リスト取得
def select_product_list():
    sql = "SELECT * FROM product WHERE stack != 0"
 
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql)
    product_list = cursor.fetchone()
        
    cursor.close()
    connection.close()
    return product_list
