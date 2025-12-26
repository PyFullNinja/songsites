from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..logs import new_log
from flask_login import login_required


admin_panel_bp = Blueprint('admin_panel', __name__)

@admin_panel_bp.route('/admin_panel')
@login_required
def admin_panel():
    if not current_user.is_admin:
        
        return 
    new_log("Пользователь зашел на страницу /admin_panel")
    return render_template('admin_panel.html')