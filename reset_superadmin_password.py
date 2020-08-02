import requests
from getpass import getpass
from argparse import ArgumentParser


def create_arg_parser():
    parser = ArgumentParser(description='AUSLM reset superadmin password tool')
    parser.add_argument('port', metavar='port', type=int, help='localhost port with reset password service')
    parser.add_argument('token', metavar='token', type=str, help='Auth token')
    return parser


def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    password = getpass('Enter new password: ')
    if not password:
        print('New password is empty, do nothing')
        return
    url = f'http://localhost:{args.port}/api/reset_superadmin_password'
    data = {
        'token': args.token,
        'new_password': password,
    }
    r = requests.post(url, json=data)
    print(r)


if __name__ == '__main__':
    main()
