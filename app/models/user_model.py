from sqlalchemy import Column, Integer, String, BigInteger
from app.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    role = Column(String(20), default="user")
     
                 