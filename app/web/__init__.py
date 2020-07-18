from flask import (Blueprint, request, redirect, url_for,
                   render_template, jsonify, abort)
from flask_login import (login_required, login_user, logout_user, current_user)

import logging
import traceback

from ..mails import send_500_email


def web_401(e):
    logging.warning('401 - [{}]'.format(e))

    return redirect(url_for('accounts_web.login', next=request.path))


def web_404(e, param):
    if current_user.is_authenticated:
        logging.warning('404 - [{}]'.format(e.description))
        message = param + " not found"

        return render_template(
           '/404.html',
            current_user=current_user,
            message=message,
        ), 404
    else:
        logging.warning('401 - [{}]'.format(e))
        return redirect(url_for('accounts_web.login'))


def web_500(e):
    logging.warning('500 - [{}]'.format(e.description))
    message = traceback.format_exc()
    err = traceback.format_exc()
    send_500_email(e, err)

    if current_user.is_authenticated:
        return render_template(
            '/500.html',
            current_user=current_user
        ), 500
    else:
        return render_template(
            '/500_not_login.html'
        ), 500
