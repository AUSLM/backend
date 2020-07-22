from argparse import ArgumentParser
import bcrypt
import logging
import urllib3

import app
from app import db #, controller
from app.config import cfg



def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    parser = ArgumentParser(description='HASLM project server')

    parser.add_argument('role', metavar='role', type=str,
                        help='A role of application instance: server or controller')
    parser.add_argument('--create-tables', action='store_true',
                        dest='create_tables',
                        help='Creates data base tables before launch.')

    args = parser.parse_args()

    logging.info('Starting server')

    if args.create_tables:
        pw = bcrypt.hashpw(str(cfg.SUPER_ADMIN_PASSWORD).encode('utf-8'), bcrypt.gensalt())
        cfg.SUPER_ADMIN_PASSWORD = ''
        db.create_tables(pw.decode('utf-8'))
    if args.role == 'server':
        logging.info('Starting HTTP server')
        app.run()
    elif args.role == 'controller':
        logging.info('Starting controller')
        controller.run()
    else:
        logging.critical('Unknown role, exit...')


if __name__ == '__main__':
    main()
