from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from ..logic import users as users_logic
from ..config import cfg
from ..auth import get_token


bp = Blueprint('users_web', __name__)


@bp.route('/management/users')
@login_required
def manage_users():
    if current_user.service_status == 'user':
        abort(404, "No rights")
    return render_template(
        '/manage_users.html',
        current_user=current_user,
        AD_USE=cfg.AD_USE
    )


@bp.route('/users')
@login_required
def users():
    if current_user.service_status == 'user':
        abort(404, "No rights")
    users = users_logic.get_users('active')
    return render_template(
        '/users.html',
        current_user=current_user,
        users=users,
        AD_USE=cfg.AD_USE
    )


@bp.route('/user/<string:email>')
@login_required
def user_page(email):
    if current_user.service_status == 'user':
        abort(404, "No rights")
    user = users_logic.get_user_info(email)
    machines = users_logic.get_user_machines(email)
    keys = users_logic.get_user_keys(email)

    return render_template(
        '/user_page.html',
        current_user=current_user,
        user=user,
        machines=machines,
        keys=keys,
        AD_USE=cfg.AD_USE
    )


@bp.route('/settings')
@login_required
def settings():
    keys = users_logic.get_user_keys(current_user.email)

    jwt_token = None
    if current_user != 'user':
        jwt_token = get_token(current_user.id)

    return render_template(
        '/settings.html',
        current_user=current_user,
        keys=keys,
        jwt_token=jwt_token,
        AD_USE=cfg.AD_USE
    )