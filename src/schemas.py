from typing import Union

from datetime import date

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: Union[str, None] = None


class UserCreate(UserBase):
    name: str


class User(UserBase):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class ReviewBase(BaseModel):
    user_id: int
    country_id: int
    rating: int
    remark: Union[str, None] = None
    feedback: Union[str, None] = None
    review_date: Union[date, None] = None

class ReviewCreate(ReviewBase):
    rating: int


class Review(ReviewBase):
    id: int
    user_id: int
    country_id: int
    rating: int
    remark: str
    feedback: str
    review_date: date

    class Config:
        from_attributes = True


class CountryBase(BaseModel):
    name: str

class CountryCreate(CountryBase):
    name: str


class Country(CountryBase):
    id: int
    name: str

    class Config:
        from_attributes = True