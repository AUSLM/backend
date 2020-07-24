from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, or_
from flask import abort
from datetime import datetime
import requests
import os
import nanoid
import logging

from ..config import cfg
from ..db import *
from .. import mails


def add_machine(e_email, addr, domain):
    with get_session() as s:
        machine = s.query(Machine).filter(
                Machine.address == addr
        ).one_or_none()

        if machine:
            if machine.status == 'active':
                abort(409, 'Machine is exist!')
            elif machine.status == 'deleted':
                machine.status = 'active'
                machine.domain = domain
        else:
            machine = Machine(address=addr, domain=domain)
            s.add(machine)
        
        s.flush()
        s.refresh(machine)

        admins = s.query(User).filter(
                or_(User.service_status == 'superadmin', User.service_status == 'admin')
        ).all()

        for admin in admins:
            access = s.query(Access).filter(
                    Access.u_id == admin.id,
                    Access.m_id == machine.id,
            ).one_or_none()
            if access:
                if access.status == 'deleted':
                    access.status == 'active'
            else:
                access = Access(u_id=admin.id, m_id=machine.id)
                s.add(access)
        
    logging.info('Adding machine [{} - {}]'.format(domain, addr))


def remove_machine(e_email, address):
    with get_session() as s:
        machine = s.query(Machine).filter(
                Machine.address == address,
                Machine.status == 'active'
        ).one_or_none()
        if not machine:
            abort(404, 'No machine with this address!')
        logging.info('Deleting machine [{}]'.format(address))

        machine.status = 'deleted'
        accesses = s.query(Access).filter(
                Access.m_id == machine.id
        ).all()
        for access in accesses:
            access.status = 'deleted'
            access.disabled = datetime.utcnow()


def get_all_machines():
    result = []
    with get_session() as s:
        machines = s.query(Machine).filter(
                Machine.status == 'active'
        ).all()

        for machine in machines:
            result.append({
                'address': machine.address,
                'domain': machine.domain,
            })
    return result


def get_machine_users(addr):
    result = []
    with get_session() as s:
        machine_users = s.query(User, Access, Machine).filter(
                User.id == Access.u_id,
                Access.m_id == Machine.id,
                Machine.address == addr,
                Access.status == 'active',
                User.service_status == 'user'
        ).all()
        for user, access, _ in machine_users:
            result.append({
                'email': user.email,
                'name': user.name,
                'surname': user.surname,
                'service_status': user.service_status,
            })
    return result


def get_domain(addr):
    with get_session() as s:
        machine =  s.query(Machine).filter(
                Machine.address == addr,
                Machine.status == 'active'
        ).one_or_none()

        if not machine:
            abort(404, 'Machine not found')

        return machine.domain


def web_terminal(U_email, address):
    with get_session() as s:
        access_exist = s.query(User, Access, Machine).filter(
                User.id == Access.u_id,
                Access.m_id == Machine.id,
                User.email == U_email,
                Machine.address == address,
                Access.status == 'active',
                Machine.status == 'active',
                User.status == 'active'
        ).one_or_none()

        if not access_exist:
            abort(409, 'No access')

        temp_password = nanoid.generate(size=20)

        machine = s.query(Machine).filter(
                Machine.address == address
        ).one_or_none()

        if not machine:
            abort(404, "Machine not found")

        #script = get_script(s, 'set_password')
        #executor.execute(machines, script, env={
        #    "LOGIN": login,
        #    "PASSWORD": temp_password
        #})
        return {
            "url": "http://{}:7080".format(address),
            "password": temp_password,
        }
