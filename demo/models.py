from database import Base
from sqlalchemy import Column, Integer, String, Float


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    description = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)
    seller_id = Column(Integer)


