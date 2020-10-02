from flask import jsonify, request, abort
import logging
import traceback
from ..mails import send_500_email


# answers

def api_ok(code, description):
    return jsonify(description=description), code


def api_4xx(code, description):
    logging.warning(f'{str(code)} - [{description}]')
    return jsonify(error=description), code


def get_json():
    data = request.get_json()
    if data is None:
        abort(415, 'Expected json')
    return data


def api_404(e):
    error = e.description
    if int(str(e.description).find('The requested URL')) + 1:
        error = 'Unknown route'
        logging.warning(f'404 - [{error}]')
    return jsonify(error=error), 404


def api_405(e):
    logging.warning('405 - [Wrong route method]')
    return jsonify(error="Wrong route method"), 405


def api_500(e):
    logging.warning(f'500 - [{e.description}]')
    err = traceback.format_exc()
    send_500_email(e, err)
    return jsonify(error="Server error, we're sorry"), 500
