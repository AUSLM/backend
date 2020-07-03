from flask import Flask, Request
from flask_login import LoginManager
from flask_mail import Mail
from gevent import monkey
from gevent.pywsgi import WSGIServer

import logging

from .config import cfg

from .auth import user_loader, header_loader

from .web import (accounts as accounts_web,
                  users as users_web,)

from .api import (accounts as accounts_api,
                  users as users_api,)

from .errors import add_error_handlers, on_json_loading_failed


app = Flask(__name__)
app.config.update(
    TEMPLATES_AUTO_RELOAD=True,
    CSRF_ENABLED=cfg.CSRF_ENABLED,
    SECRET_KEY=cfg.SECRET_KEY,
    AUTH_HEADER_NAME=cfg.AUTH_HEADER_NAME,
    MAIL_SERVER=cfg.MAIL_SERVER,
    MAIL_PORT = cfg.MAIL_PORT,
    MAIL_USERNAME = cfg.MAIL_USERNAME,
    MAIL_PASSWORD = cfg.MAIL_PASSWORD,
    MAIL_DEFAULT_SENDER = cfg.MAIL_DEFAULT_SENDER,
    MAIL_USE_SSL = True,
)

app.register_blueprint(accounts_web.bp)
app.register_blueprint(users_web.bp)

app.register_blueprint(accounts_api.bp, url_prefix='/api')
app.register_blueprint(users_api.bp, url_prefix='/api/user')

add_error_handlers(app)
Request.on_json_loading_failed = on_json_loading_failed

mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(user_loader)
#login_manager.header_loader(auth.header_loader)

logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',
                    level=logging.INFO)


def run():
    monkey.patch_all(ssl=false)
    http_server = WSGIServer((cfg.HOST, cfg.PORT), app)
    logging.info('Started server')
    http_server.serve_forever()
