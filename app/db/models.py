from sqlalchemy import (Column, Integer, String, ForeignKey,
                        DateTime, Boolean, UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ENUM, UUID, TEXT
from flask_login import UserMixin

from datetime import datetime
import uuid

from ..config import cfg


Base = declarative_base()

Status = ENUM('active', 'deleted', 'banned', 'unconfirmed', name='status')

Service_status = ENUM('superadmin', 'admin', 'user', name='service_status')


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    cookie_id = Column(UUID(as_uuid=True), default=uuid.uuid4,
                       unique=True, nullable=False)
    confirmation_link = Column(String, unique=True, nullable=False)
    status = Column(Status, default=cfg.DEFAULT_USER_STATUS, nullable=False)

    email = Column(String, unique=True, nullable=False)
    password = Column(TEXT, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    service_status = Column(Service_status, default='user', nullable=False)

    def get_id(self):
        return self.cookie_id


class Machine(Base):
    __tablename__ = 'machines'

    id = Column(Integer, primary_key=True)
    status = Column(Status, default='active', nullable=False)
    sshd_pid = Column(Integer)
    agent_pid = Column(Integer)

    address = Column(String, unique=True, nullable=False)
    domain = Column(String)


class Access(Base):
    __tablename__ = 'accesses'

    id = Column(Integer, primary_key=True)
    u_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    m_id = Column(Integer, ForeignKey('machines.id'), nullable=False)
    status = Column(Status, default='active', nullable=False)

    issued = Column(DateTime, default=datetime.utcnow, nullable=False)
    disabled = Column(DateTime)


class PublicKey(Base):
    __tablename__ = 'public_keys'

    id = Column(Integer, primary_key=True)
    u_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(Status, default='active', nullable=False)

    body = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    update_time = Column(DateTime, default=datetime.utcnow, nullable=False)


# Some jwt api stuff

class Token(Base):
    __tablename__ = 'tokens'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    u_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(Status, default='active', nullable=False)

    issued = Column(DateTime, default=datetime.utcnow, nullable=False)
