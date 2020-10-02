import logging
from flask_mail import Message
import os
import datetime
import traceback

import app
from .config import cfg


def log_file_email_errors(e):
    if not os.path.exists('send_email_errors.txt'):
        file = open('send_email_errors.txt', 'w')
        file.close()

    with open('send_email_errors.txt', 'a+') as f:
        f.write(datetime.datetime.now().isoformat())
        f.write('\n')
        f.write(traceback.format_exc())
        f.write('\n')


def send_link_email(email, link, event):
    try:
        if cfg.AD_USE:
            msg = Message(
                body = f'You has been invited to {cfg.SITE_ADDRESS}',
                subject = f'AUSLM invite',
                recipients = [email]
            )
        else:
            msg = Message(
                body = f'{cfg.SITE_ADDRESS}/{event}/{link}',
                subject = f'AUSLM {event} link',
                recipients = [email]
            )
        app.mail.send(msg)
        logging.info(f'Sending {event} message to {email}')
    except Exception as e:
        log_file_email_errors(e)


def send_reset_email(email, new_password):
    try:
        msg = Message(
            body = f'Your new password - {new_password}',
            subject = 'AUSLM password reset',
            recipients = [email]
        )
        app.mail.send(msg)
        logging.info(f'Sending password reset message to {email}')
    except Exception as e:
        log_file_email_errors(e)


def send_500_email(e, error):
    try:
        msg = Message(
            body = error,
            subject = 'AUSLM 500 server error',
            recipients = [cfg.SUPER_ADMIN_MAIL]
        )
        app.mail.send(msg)
        logging.info('Sending 500 error message')
    except Exception as e:
        log_file_email_errors(e)
