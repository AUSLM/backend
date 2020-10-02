from flask import Blueprint, redirect, render_template, abort
from flask_login import login_required, current_user

from ..logic import general as general_logic


bp = Blueprint('general_web', __name__)


@bp.route('/')
@login_required
def home():
    if current_user.service_status == 'user':
        return redirect('/machines')
    return render_template(
        '/home.html',
        current_user=current_user
    )


@bp.route('/instructions')
@login_required
def instructions():
    return render_template(
        '/instructions.html',
        current_user=current_user
    )


@bp.route('/logs/activity')
@login_required
def activity_logs():
    if current_user.service_status == 'user':
        abort(404, "No rights")
    logs = general_logic.get_activity_logs()
    return render_template(
        '/activity_logs.html',
        current_user=current_user,
        logs=logs
    )


@bp.route('/logs/controller')
@login_required
def controller_logs():
    if current_user.service_status == 'user':
        abort(404, "No rights")
    logs = general_logic.get_controller_logs()
    return render_template(
        '/controller_logs.html',
        current_user=current_user,
        logs=logs
    )
