from flask import Blueprint, redirect, url_for, render_template, abort
from flask_login import login_required, logout_user, current_user

from ..logic import accounts as accounts_logic
from ..config import cfg


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


@bp.route('/confirm/<string:link>')
def confirm(link):
    if cfg.AD_USE:
        abort(404, "Page not found")
    answer = accounts_logic.confirm_user(link)
    return render_template(
        '/confirmation.html',
        answer=answer
    )


@bp.route('/invite/<string:link>')
def invite(link):
    if cfg.AD_USE:
        abort(404, "Page not found")
    info = accounts_logic.find_invited_user(link)
    return render_template(
        '/invitation.html',
        user=info['user'] if 'user' in info else '',
        error=info['error'] if 'error' in info else ''
    )


@bp.route('/reset-password')
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('.login'))
    return render_template(
        '/reset_password.html'
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
