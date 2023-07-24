from flask import Flask, Blueprint, render_template, request
import psycopg2, os
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


#DB接続
def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

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


#商品追加画面へ遷移
@admin_bp.route('/adp')
def add_product():
    return render_template('admin/add_product.html')

#追加確認画面へ遷移
@admin_bp.route('/add_product', methods=['POST'])
def ap_conf():
    name = request.form.get('name')
    gold = request.form.get('gold')
    stack = request.form.get('stack')
    return render_template('admin/add_product_conf.html', name=name, gold=gold, stack=stack)

#追加確定画面へ遷移
@admin_bp.route('/ap_exe', methods=['POST'])
def ap_exe():
    name = request.form.get('name')
    gold = request.form.get('gold')
    stack = request.form.get('stack')
    print('ap_exe' + name +gold + stack)
    ap_sql(name, gold, stack)
    product_list = select_product_list()
    return render_template('admin/add_product_exe.html', name=name, gold=gold, stack=stack, product_list=product_list)


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
###############################################################        

#商品削除画面へ遷移
@admin_bp.route('/dp')
def delete_product():
    product_list = select_product_list()
    return render_template('admin/delete_product.html', product_list=product_list)

#削除確認画面へ遷移
@admin_bp.route('/delete_product', methods=['POST'])
def delete_conf():
    name = request.form.get('name')
    gold = request.form.get('gold')
    stack = request.form.get('stack')
    return render_template('admin/delete_product_conf.html', name=name,gold=gold, stack=stack )

#削除確定画面へ遷移
@admin_bp.route('/delete_exe', methods=['POST'])
def delete_exe():
    name = request.form.get('name')
    gold = request.form.get('gold')
    stack = request.form.get('stack')
    print('ap_exe' + name +gold + stack)
    dp_sql(name)
    product_list = select_product_list()
    return render_template('admin/delete_product_exe.html', name=name, gold=gold, stack=stack, product_list=product_list)



#DBから削除
def dp_sql(name):
    sql = 'DELETE FROM product WHERE name = %s'
    count = 0
    try :
        
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (name,))
        connection.commit()
    except psycopg2.DatabaseError:
        count = 1
    finally :
        connection.close()
        cursor.close()
    if count ==  1:
        return 0
    else :
        return 
############################################################
#商品更新画面へ遷移
@admin_bp.route('/up')
def update_product():
    product_list = select_product_list()
    return render_template('admin/update_product.html', product_list=product_list)

#更新確認画面へ遷移
@admin_bp.route('/update_product', methods=['POST'])
def update_conf():
    name = request.form.get('name')
    gold = request.form.get('gold')
    stack = request.form.get('stack')
    return render_template('admin/update_product_conf.html', name=name,gold=gold, stack=stack )

#更新確定画面へ遷移
@admin_bp.route('/update_exe', methods=['POST'])
def update_exe():
    name = request.form.get('name')
    gold = request.form.get('gold')
    stack = request.form.get('stack')
    print('ap_exe' + name +gold + stack)
    up_sql(stack, name)
    product_list = select_product_list()
    return render_template('admin/update_product_exe.html', name=name, gold=gold, stack=stack, product_list=product_list)



#DB更新
def up_sql(stack, name):
    sql = 'UPDATE product SET stack = %s WHERE name= %s;'
    count = 0
    try :
        
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (stack, name))
        connection.commit()
    except psycopg2.DatabaseError:
        count = 1
    finally :
        connection.close()
        cursor.close()
    if count ==  1:
        return 0
    else :
        return 
    
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