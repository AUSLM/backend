from flask import jsonify, request, abort
import logging
import traceback
from ..mails import send_500_email


# answers

def make_ok(code, description):
    return jsonify(description=description), code


def make_4xx(code, description):
    logging.warning(str(code) + ' - [{}]'.format(description))
    return jsonify(error=description), code


def get_json():
    data = request.get_json()
    if data is None:
        abort(415, 'Expected json')
    return data


def make_404(e):
    error = e.description
    if int(str(e.description).find('The requested URL')) + 1:
        error = 'Unknown route'
        logging.warning('404 - [{}]'.format(error))
    return jsonify(error=error), 404


def make_405(e):
    logging.warning('405 - [{}]'.format(e))
    return jsonify(error="Wrong route method"), 405


def server_500_error(e):
    logging.warning('500 - [{}]'.format(e.description))
    err = traceback.format_exc()
    send_500_email(e, err)
    return jsonify(error="Server error, we're sorry"), 500
