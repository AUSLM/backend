from argparse import ArgumentParser
import bcrypt
import logging
import urllib3

import app
from app import db
from app.config import cfg


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    parser = ArgumentParser(description='HASLM project server')

    parser.add_argument('--create-tables', action='store_true',
                        dest='create_tables',
                        help='Creates data base tables before launch.')

    args = parser.parse_args()

    logging.info('Starting server')
    db.check_database()

    if args.create_tables:
        pw = bcrypt.hashpw(str(cfg.SUPER_ADMIN_PASSWORD).encode('utf-8'), bcrypt.gensalt())
        cfg.SUPER_ADMIN_PASSWORD = ''
        db.create_tables(pw.decode('utf-8'))
    logging.info('Starting HTTP server')
    app.run()


if __name__ == '__main__':
    main()
