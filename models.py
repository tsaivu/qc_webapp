from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
import uuid
from datetime import datetime
from pytz import timezone


def gen_uuid():
    return str(uuid.uuid4())


def get_vn_time():
    return datetime.now(timezone('Asia/Ho_Chi_Minh'))


class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String)
    role = Column(String)


class Machine(Base):
    __tablename__ = 'machines'
    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String)


class Product(Base):
    __tablename__ = 'products'
    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String)


class QCCheck(Base):
    __tablename__ = 'qc_snapshot_checks'
    id = Column(String, primary_key=True, default=gen_uuid)
    timestamp = Column(DateTime(timezone=True), default=get_vn_time) 
    user_id = Column(String, ForeignKey('users.id'))
    product_id = Column(String, ForeignKey('products.id'))
    machine_id = Column(String, ForeignKey('machines.id'))
    image_path = Column(Text)

    user = relationship("User")
    product = relationship("Product")
    machine = relationship("Machine")
