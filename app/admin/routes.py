from flask import Blueprint, render_template

admin = Blueprint('admin', __name__)

@admin.route('/admin')
def admin_index():
    return render_template('admin/some_admin_page.html')