from flask import Blueprint, jsonify, request, abort
from flask_login import (login_required, login_user, logout_user, current_user)

from . import *
from ..logic import accounts as accounts_logic
from ..auth import pre_login
from ..validation.validation import validate
from ..validation import schemas


bp = Blueprint('accounts_api_web', __name__)


@bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return make_4xx(409, 'User is currently authenticated')

    data = validate(get_json(), schemas.login)
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

    data = validate(get_json(), schemas.register)
    accounts_logic.register_user(data['email'], data['password'],
                                 data['name'], data['surname'])
    return make_ok(201, 'User was registered')


@bp.route('/confirm/<link>', methods=['GET'])
def confirm(link):
    accounts_logic.confirm_user(link)
    return make_ok(200, 'User was confirmed')


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
