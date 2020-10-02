from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user


bp = Blueprint('accesses_web', __name__)


@bp.route('/management/accesses')
@login_required
def manage_accesses():
    if current_user.service_status == 'user':
        abort(404, "No rights")
    return render_template(
        '/manage_accesses.html',
        current_user=current_user
    )
