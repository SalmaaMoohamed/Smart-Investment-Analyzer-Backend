from sqlalchemy import Column, Integer, String
from auth.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)   # ETEL
    symbol = Column(String, unique=True) # ETEL.CA
    image_url = Column(String)           # صورة السهم
