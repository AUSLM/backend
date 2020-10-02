from flask import abort
import bcrypt
import nanoid
import uuid
import logging

from ..config import cfg
from ..db import *
from ..auth import ldap_login
from .. import mails
from .general import save_log


def ldap_check_register(email):
    with get_session() as s:
        user = s.query(User).filter(
                User.email == email
        ).one_or_none()

        if user:
            if user.status == 'deleted':
                user.status = cfg.DEFAULT_USER_STATUS
            else:
                return
        else:
            # ldap get user name and surname TODO
            name = "LDAP_Name"
            surname = "LDAP_Surname"
            user = User(email=email, password='-', name=name, surname=surname,
                        confirmation_link='-', status='active')
            s.add(user)

            s = save_log(s, email, 'registerd', 'as LDAP user')
            logging.info(f'Registering new user [{email}]')


def register_user(email, password, name, surname):
    with get_session() as s:
        user = s.query(User).filter(
                User.email == email
        ).one_or_none()

        confirmation_link = ''
        while True:
            confirmation_link = nanoid.generate(size=50)
            exists = s.query(User).filter(
                    User.confirmation_link == confirmation_link
            ).one_or_none()
            if not exists:
                break

        if user:
            if user.status == 'deleted':
                user.name = name
                user.surname = surname
                user.status = cfg.DEFAULT_USER_STATUS
                user.confirmation_link = confirmation_link
                pw = bcrypt.hashpw(str(password).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                user.password = pw
            elif user.status == 'banned':
                abort(409, 'User with this email was banned')
            else:
                abort(409, 'Trying to register existing user')
        else:
            user = User(email=email, password='-', name=name, surname=surname,
                        confirmation_link=confirmation_link)
            pw = bcrypt.hashpw(str(password).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user.password = pw
            s.add(user)

        if cfg.DEFAULT_USER_STATUS == 'unconfirmed':
            mails.send_link_email(email, confirmation_link, 'confirm')

        s = save_log(s, email, 'registered', '')
        logging.info(f'Registering new user [{email}]')


def confirm_user(confirmation_link):
    with get_session() as s:
        user = s.query(User).filter(
                User.confirmation_link == confirmation_link
        ).one_or_none()
        if not user or user.status != 'unconfirmed':
            return 'Confirmation error'
        user.status = 'active'

        s = save_log(s, user.email, 'confirmed', '')
        logging.info(f'User [{user.email}] is confirmed')
        return "Confirmed successfully"


def reset_password(email):
    with get_session() as s:
        user = s.query(User).filter(
                User.email == email,
                User.status == 'active',
        ).one_or_none()

        if not user:
            abort(404, 'Invalid user')
        
        new_password = nanoid.generate(size=20)
        npw = bcrypt.hashpw(str(new_password).encode('utf-8'), bcrypt.gensalt())
        user.password = npw.decode('utf-8')
        user.cookie_id = uuid.uuid4()
        mails.send_reset_email(email, new_password)


def change_password(u_id, old_password, new_password):
    if old_password == new_password:
        abort(409, 'Old and new passwords are equal')
    with get_session() as s:
        user = s.query(User).get(u_id)

        opw = str(old_password).encode('utf-8')
        npw = str(new_password).encode('utf-8')
        pw = str(user.password).encode('utf-8')

        if not bcrypt.checkpw(opw, pw):
            abort(422, 'Invalid password')
        npw = bcrypt.hashpw(npw, bcrypt.gensalt())
        user.password = npw.decode('utf-8')
        user.cookie_id = uuid.uuid4()
        return user


def close_all_sessions(u_id, password):
    with get_session() as s:
        user = s.query(User).get(u_id)

        if cfg.AD_USE and user.email != cfg.SUPER_ADMIN_MAIL:
            if not ldap_login(email, password):
                abort(422, 'Invalid password')
        else:
            ipw = str(password).encode('utf-8')
            pw = str(user.password).encode('utf-8')
            if not bcrypt.checkpw(ipw, pw):
                abort(422, 'Invalid password')
        user.cookie_id = uuid.uuid4()
        return user


# for admins

def superadmin_reset_password(token, new_password):
    if not token == cfg.SUPER_ADMIN_TOKEN:
        abort(422, 'Wrong superadmin token')

    with get_session() as s:
        superadmin = s.query(User).filter(
                User.email == cfg.SUPER_ADMIN_MAIL
        ).one_or_none()

        npw = bcrypt.hashpw(str(new_password).encode('utf-8'), bcrypt.gensalt())
        superadmin.password = npw.decode('utf-8')

        s = save_log(s, 'Superadmin', 'reseted password', '')
        logging.info("Superadmin's password was reseted")


def invite_user(e_email, u_email):
    if cfg.AD_USE:
        invite_AD_user(e_email, u_email)
    else:
        invite_general_user(e_email, u_email)


def invite_AD_user(e_email, u_email):
    with get_session() as s:
        user = s.query(User).filter(
                User.email == u_email
        ).one_or_none()

        if user:
            if user.status == 'active':
                abort(409, 'Trying to invite existing user')

        # ldap get user name and surname TODO
        name = "LDAP_Name"
        surname = "LDAP_Surname"
        user = User(email=u_email, password='-', name=name, surname=surname,
                    confirmation_link='-', status='active')
        s.add(user)

        mails.send_link_email(u_email, '-', 'invite')

        s = save_log(s, u_email, 'invited', 'as LDAP user')
        logging.info(f'Invited new user [{u_email}]')


def invite_general_user(e_email, u_email):
    with get_session() as s:
        user = s.query(User).filter(
                User.email == u_email
        ).one_or_none()

        if user:
            if user.status == 'active':
                abort(409, 'Trying to invite existing user')


        confirmation_link = ''
        while True:
            confirmation_link = nanoid.generate(size=50)
            exists = s.query(User).filter(
                    User.confirmation_link == confirmation_link
            ).one_or_none()
            if not exists:
                break

        user = User(email=u_email, password='-', name='-', surname='-',
                    confirmation_link=confirmation_link, status='unconfirmed')
        s.add(user)

        mails.send_link_email(u_email, confirmation_link, 'invite')

        s = save_log(s, u_email, 'invited', '')
        logging.info(f'Invited new user [{u_email}]')


def find_invited_user(invitational_link):
    with get_session() as s:
        user = s.query(User).filter(
                User.confirmation_link == invitational_link
        ).one_or_none()
        if not user or user.status != 'unconfirmed':
            return {'error': 'Invitation error'}

        return {'user': user.email}


def confirm_invite(email, password, name, surname):
    with get_session() as s:
        kuser = s.query(User).filter(
                User.email == email
        ).one_or_none()

        print(kuser.status)

        user = s.query(User).filter(
                User.email == email,
                User.status != 'active'
        ).one_or_none()

        if not user:
            abort(404, 'User not found')

        user.password = bcrypt.hashpw(str(password).encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.name = name
        user.surname = surname
        user.status = 'active'

        s = save_log(s, email, 'confirmed invite', '')
        logging.info(f'Confirmed invite for new user [{email}]')


def delete_user(e_email, u_email):
    with get_session() as s:
        user = s.query(User).filter(
                User.email == u_email,
                User.status == 'active',
                User.service_status != 'superadmin'
        ).one_or_none()

        if not user:
            abort(404, 'User not found')
        user.status = 'deleted'

        keys = s.query(PublicKey).filter(
                PublicKey.u_id == user.id
        ).all()
        for key in keys:
            key.status = 'deleted'

        accesses = s.query(Access).filter(
                Access.u_id == user.id
        ).all()
        for access in accesses:
            access.status == 'deleted'

        s = save_log(s, e_email, "Deleted user", u_email)
        logging.info(f'User [{u_email}] was deleted')


def change_privileges(u_email, role):
    with get_session() as s:
        user = s.query(User).filter(
                User.email == u_email,
                User.status == 'active',
        ).one_or_none()

        if not user:
            abort(404, 'No user with this email')
        if user.service_status == 'superadmin':
            abort(409, "Can't change superadmin privileges!")
        if user.service_status == role:
            abort(409, 'User already has that role')
        user.service_status = role

        if role == 'admin':
            machines = s.query(Machine).filter(
                    Machine.status == 'active'
            ).all()

            for machine in machines:
                access = s.query(Access).filter(
                        Access.u_id == user.id,
                        Access.m_id == machine.id,
                ).one_or_none()

                if access:
                    if access.status == 'deleted':
                        access.status == 'active'
                else:
                    access = Access(u_id=user.id, m_id=machine.id)
                    s.add(access)

            s = save_log(s, 'Superadmin', "granted admin's rights", f'to {u_email}')
            logging.info(f"Grant {u_email} admin's rights")
        elif role == 'user':
            accesses = s.query(Access).filter(
                    Access.u_id == user.id
            ).all()

            for access in accesses:
                access.status == 'deleted'

            s = save_log(s, 'Superadmin', "revoked admin's rights", f'from {u_email}')
            logging.info(f"Revoke admin's rights from {u_email}")
        else:
            abort(409, 'Unknown role')


def get_admins():
    result = []
    with get_session() as s:
        admins = s.query(User).filter(
                User.status == 'active',
                User.service_status == 'admin'
        ).all()

        for admin in admins:
            result.append({
                'email': admin.email,
                'name': admin.name,
                'surname': admin.surname
            })
    return result
