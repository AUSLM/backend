from types import SimpleNamespace
import os


cfg = SimpleNamespace()


def _get_db_connection_string():
    db_connection_string = os.getenv('DB_CONNECTION_STRING')
    if db_connection_string:
        return db_connection_string
    return 'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'.format(**os.environ)


cfg.CSRF_ENABLED = False if os.getenv('DISABLE_CSRF') else True
cfg.SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))
cfg.AUTH_HEADER_NAME = os.getenv('AUTH_HEADER_NAME', 'X-AUSLM-Token')

cfg.HOST = os.getenv('HOST_ADDR', '0.0.0.0')
cfg.PORT = int(os.getenv('PORT', '8080'))
cfg.DB_CONNECTION_STRING = _get_db_connection_string()
cfg.RUNTIME_FOLDER = os.path.dirname(os.path.abspath(__file__))
cfg.SCRIPTS_FOLDER = os.getenv('SCRIPT_FOLDER', f'{cfg.RUNTIME_FOLDER}/scripts')

cfg.AD_USE = True if os.getenv('AD_USE') == "True" else False
cfg.AD_SERVER_ADDRESS = os.getenv('AD_SERVER_ADDRESS', 'localhost')

cfg.DEFAULT_USER_STATUS = os.getenv('DEFAULT_USER_STATUS')

cfg.SITE_ADDRESS = os.getenv('SITE_ADDRESS')

cfg.SUPER_ADMIN_MAIL = os.getenv('SUPER_ADMIN_MAIL')
cfg.SUPER_ADMIN_PASSWORD = os.getenv('SUPER_ADMIN_PASSWORD')

cfg.SUPER_ADMIN_TOKEN = os.getenv('SUPER_ADMIN_TOKEN')
cfg.RESET_SUPER_ADMIN_PASSWORD_FROM_ANYWHERE = True if os.getenv('RESET_SUPER_ADMIN_PASSWORD_FROM_ANYWHERE') == "True" else False

cfg.MAIL_SERVER = os.getenv('MAIL_SERVER')
cfg.MAIL_PORT = os.getenv('MAIL_PORT')
cfg.MAIL_USERNAME = os.getenv('MAIL_USERNAME')
cfg.MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
cfg.MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

#cfg.AGENT_PORT = int(os.getenv('AGENT_PORT', 9442))
#cfg.EXECUTOR_WORKERS = int(os.getenv('EXECUTOR_WORKERS', 4))
