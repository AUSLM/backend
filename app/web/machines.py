from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

from ..logic import users as users_logic, machines as machines_logic


bp = Blueprint('machines_web', __name__)


@bp.route('/management/machines')
@login_required
def manage_machines():
    if current_user.service_status == 'user':
        abort(404, "No rights")
    return render_template(
        '/manage_machines.html',
        current_user=current_user
    )


@bp.route('/machines')
@login_required
def machines():
    machines = []
    if current_user.service_status == 'user':
        machines = users_logic.get_user_machines(current_user.email)
    else:
        machines = machines_logic.get_all_machines()
    return render_template(
        '/machines.html',
        current_user=current_user,
        machines=machines
    )


@bp.route('/machine/<string:address>')
@login_required
def machine_page(address):
    if current_user.service_status == 'user':
        abort(404, "No rights")
    domain = machines_logic.get_domain(address)
    users = machines_logic.get_machine_users(address)

    return render_template(
        '/machine_page.html',
        current_user=current_user,
        address=address,
        domain=domain,
        users=users
    )
