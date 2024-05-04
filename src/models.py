from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    email = Column(String)

class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    country_id = Column(Integer, ForeignKey("country.id"))
    rating = Column(Integer)
    remark = Column(String)
    feedback = Column(String)
    review_date = Column(Date)

class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True)
    name = Column(String)
