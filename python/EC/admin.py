from flask import Flask, Blueprint, render_template, request
import psycopg2, os
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/admin')
def add_product():
    return render_template('admin/add_product.html')

