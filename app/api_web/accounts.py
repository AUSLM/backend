from flask import Blueprint, redirect, url_for
from flask_login import (login_required, login_user, logout_user, current_user)

from . import *
from ..logic import accounts as accounts_logic
from ..auth import pre_login, reissue_token
from ..validation.validation import validate
from ..validation import schemas
from ..config import cfg


bp = Blueprint('accounts_api_web', __name__)


@bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return make_4xx(409, 'User is currently authenticated')

    data = validate(get_json(), schemas.login)
    if cfg.AD_USE:
        accounts_logic.ldap_check_register(data['email'])
    user = pre_login(data['email'], data['password'])
    login_user(user)
    if 'next' in data:
        return redirect(url_for(data['next']))
    return make_ok(200, 'User was logined')


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return make_ok(200, 'User was logouted')


@bp.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return make_4xx(409, 'User is currently authenticated')
    if cfg.AD_USE:
        return make_4xx(404, 'Unknown route')

    data = validate(get_json(), schemas.register)
    accounts_logic.register_user(data['email'], data['password'],
                                 data['name'], data['surname'])
    return make_ok(201, 'User was registered')


@bp.route('/confirm/<link>', methods=['GET'])
def confirm(link):
    if cfg.AD_USE:
        return make_4xx(404, 'Unknown route')
    accounts_logic.confirm_user(link)
    return make_ok(200, 'User was confirmed')


@bp.route('/issue_token', methods=['GET'])
@login_required
def issue_token():
    if current_user.service_status == 'user':
        return make_4xx(404, 'Unknown route')
    token = reissue_token(current_user.id)
    return make_ok(200, token)


@bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    if cfg.AD_USE:
        abort(409, "Change your password in company's auth system")
    data = validate(get_json(), schemas.change_password)
    user = accounts_logic.change_password(current_user.id,
                                          data['old_password'],
                                          data['new_password'])
    login_user(user)
    return make_ok(200, 'Changed')


@bp.route('/close_all_sessions', methods=['POST'])
@login_required
def close_all_sessions():
    data = validate(get_json(), schemas.password)
    user = accounts_logic.close_all_sessions(current_user.id, data['password'])
    login_user(user)
    return make_ok(200, 'Logout from all other sessions')


@bp.route('/reset_password', methods=['POST'])
def reset_password():
    if cfg.AD_USE:
        abort(409, "Change your password in company's auth system")
    data = validate(get_json(), schemas.password)
    accounts_logic.reset_password(data['password'])
    return make_ok(200, 'Successfully reseted - check your email')


@bp.route('/add_admin', methods=['POST'])
@login_required
def add_admin():
    if current_user.service_status != 'superadmin':
        return make_4xx(404, 'Unknown route')
    data = validate(get_json(), schemas.manage_admin)
    accounts_logic.change_privileges(data['email'], 'admin')
    return make_ok(200, "Admin rights was granted")


@bp.route('/remove_admin', methods=['POST'])
@login_required
def remove_admin():
    if current_user.service_status != 'superadmin':
        return make_4xx(404, 'Unknown route')
    data = validate(get_json(), schemas.manage_admin)
    accounts_logic.change_privileges(data['email'], 'user')
    return make_ok(200, "Admin rights was removed")


@bp.route('/reset_superadmin_password', methods=['POST'])
def reset_superadmin_password():
    if not cfg.RESET_SUPER_ADMIN_PASSWORD_FROM_ANYWHERE and not request.host == "localhost:" + str(cfg.PORT):
        abort(404, 'Unknown route')

    data = validate(get_json(), schemas.superadmin_reset_password)
    accounts_logic.superadmin_reset_password(data['token'], data['new_password'])
    return make_ok(200, 'Changed')
