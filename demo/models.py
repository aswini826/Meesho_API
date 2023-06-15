from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    description = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    seller_id = Column(Integer, unique=True)


class Catagory(Base):
    __tablename__ = 'catagory'

    id = Column(Integer, primary_key=True, index=True)
    catagory_id = Column(Integer, ForeignKey(Users.id))
    name = Column(String, unique=True)
    description = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey(Catagory.id))
    customer_name = Column(String)
    email = Column(String, unique=True)
    age = Column(Integer)
    gender = Column(String)
    phone = Column(String)
