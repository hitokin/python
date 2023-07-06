from flask import Flask, Blueprint, render_template, request
import psycopg2, os
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

#DB接続
def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection



#商品追加画面へ遷移
@admin_bp.route('/admin')
def add_product():
    return render_template('admin/add_product.html')


#追加確認画面へ遷移
@admin_bp.route('/add_product', methods=['POST'])
def ap_conf():
    name = request.form.get('name')
    gold = request.form.get('gold')
    stack = request.form.get('stack')
    return render_template('admin/add_product_conf.html', name=name, gold=gold, stack=stack)


#DBへ追加
def ap_sql(name, gold, stack):
    sql = 'INSERT INTO product (name, gold, stack) VALUES(%s, %s, %s)'
    name = str(name)
    gold = str(gold)
    stack = str(stack)
    count = 0
    try :
        
        connection = get_connection()
        cursor = connection.cursor()
        print('ap_sql' + name, gold, stack)
        cursor.execute(sql, (name, gold, stack))
        connection.commit()
    except psycopg2.DatabaseError:
        count = 1
    finally :
        connection.close()
        cursor.close()
    if count ==  1:
        return 0
    else :
        return name, gold, stack
        


#追加確定画面へ遷移
@admin_bp.route('/ap_exe', methods=['POST'])
def ap_exe():
    name = request.form.get('name')
    gold = request.form.get('gold')
    stack = request.form.get('stack')
    print('ap_exe' + name +gold + stack)
    ap_sql(name, gold, stack)
    return render_template('admin/add_product_exe.html', name=name, gold=gold, stack=stack)