from flask import (Blueprint, request, redirect, url_for,
                   render_template, jsonify, abort)
from flask_login import (login_required, login_user, logout_user, current_user)

from ..logic import accounts as accounts_logic
from ..config import cfg

import logging


bp = Blueprint('accounts_web', __name__)


@bp.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect('/')
    return render_template(
        '/login.html',
        AD_USE=cfg.AD_USE
    )


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))


@bp.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('.login'))
    return render_template(
        '/register.html',
        AD_USE=cfg.AD_USE
    )


@bp.route('/permissions')
@login_required
def permissions():
    if current_user.service_status == 'user':
        abort(404, "No rights")
    admins = accounts_logic.get_admins()
    return render_template(
        '/permissions.html',
        current_user=current_user,
        admins=admins
    )
