from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_review(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.id == review_id).first()


def get_review_by_user_id(db: Session, user_id: int):
    return db.query(models.Review).filter(models.Review.user_id == user_id).first()

def get_reviews_by_country_id(db: Session, country_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Review).filter(models.Review.country_id == country_id).offset(skip).limit(limit).all()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_reviews_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Review).filter(models.Review.user_id == user_id).offset(skip).limit(limit).all()


def get_reviews(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Review).offset(skip).limit(limit).all()


def create_review(db: Session, review: schemas.ReviewCreate):
    db_review = models.Review(user_id=review.user_id, country_id=review.country_id, rating=review.rating, remark=review.remark, feedback=review.feedback, review_date=review.review_date)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_countries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Country).offset(skip).limit(limit).all()

def get_country_by_name(db: Session, name: str):
    return db.query(models.Country).filter(models.Country.name == name).first()

def get_country_by_country_id(db: Session, country_id: int):
    return db.query(models.Country).filter(models.Country.id == country_id).first()


def create_country(db: Session, country: schemas.CountryCreate):
    db_country = models.Country(name=country.name)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country