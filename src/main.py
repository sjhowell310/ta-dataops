# import camelot

import json
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

import camelot
import pandas as pd
from datetime import date

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_email = crud.get_user_by_email(db, email=user.email)
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user and db_email:
        return {"message": f"User '{user.name}' already registered..."}
    return crud.create_user(db=db, user=user)

@app.post("/countries/", response_model=schemas.Country)
def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    db_country = crud.get_country_by_name(db, name=country.name)
    if db_country:
        return {"message": f"Country '{country.name}' already registered, skipping..."}
    return crud.create_country(db=db, country=country)

@app.get("/countries/name/{name}", response_model=schemas.Country)
def read_country(name: str, db: Session = Depends(get_db)):
    db_country = crud.get_country_by_name(db, name=name)
    return db_country

@app.get("/countries/id/{country_id}", response_model=schemas.Country)
def read_country(country_id: int, db: Session = Depends(get_db)):
    """Retrieve country record according to country id from SQLite backend

    Args:
        country_id (int): Unique identifier of the country
        db (Session, optional): Session used to interact with SQLite backend. Defaults to Depends(get_db).

    Returns:
        Country: Serialized object representation of Country table entry.
    """
    db_country = crud.get_country_by_country_id(db, country_id=country_id)
    return db_country

@app.get("/countries/", response_model=list[schemas.Country])
def read_countries(db: Session = Depends(get_db)):
    db_country = crud.get_countries(db)
    return db_country


@app.get("/home")
def root():
    return {"message": "Hello, Reviews party time to come"}

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/id/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/name/{name}", response_model=schemas.User)
def read_user(name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, name=name)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# @app.post("/users/{user_id}/{country_id}/review/", response_model=schemas.Review)
# def create_review_for_user(
#     user_id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_review(db=db, user_id=user_id, review=review)

@app.post("/reviews/", response_model=schemas.Review)
def create_review(
    review: schemas.ReviewCreate, db: Session = Depends(get_db)
):
    return crud.create_review(db=db, review=review)


@app.get("/reviews/", response_model=list[schemas.Review])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = crud.get_reviews(db, skip=skip, limit=limit)
    return reviews


@app.get("/reviews/user/{user_id}", response_model=list[schemas.Review])
def read_reviews(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = crud.get_reviews_by_user_id(db, user_id=user_id, skip=skip, limit=limit)
    return reviews

@app.get("/reviews/country/{country_id}", response_model=list[schemas.Review])
def read_reviews(country_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = crud.get_reviews_by_country_id(db, country_id=country_id, skip=skip, limit=limit)
    return reviews

@app.get("/load_db")
def load_reviews_db(db: Session = Depends(get_db)):
    reviews: pd.DataFrame = camelot.read_pdf("dataops_tp_reviews_-_dataops_tp_reviews.pdf")[0].df[1:]

    feedback: pd.DataFrame = reviews.rename({0:"name",1:"remark",2:"rating",3:"feedback",4:"email",5:"country",6:"review_date"}, axis='columns')
    feedback["rating"] = feedback["feedback"].str[0]
    feedback["feedback"] = feedback["feedback"].str[2:]

    load_countries(feedback["country"].tolist(), db)
    load_users(feedback[["name", "email"]], db)
    load_reviews(feedback[["name","remark", "rating", "feedback", "country", "review_date"]], db)

def load_countries(countries: list[str], db: Session):
    for country in countries:
        create_country(country=schemas.CountryCreate(name=country), db=db)

def load_users(df: pd.DataFrame, db: Session):
    df["email"] = df["email"].where((df["email"].str.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$')), other="N/A")
    for value in df.values.tolist():
        # requests.put("http://127.0.0.1:8000/users/", data=json.dumps({"name": f"{value[0]}", "email": f"{value[1]}"}))
        create_user(user=schemas.UserCreate(name=value[0], email=value[1]), db=db)

def load_reviews(df: pd.DataFrame, db: Session):
    for value in df.values.tolist():
        user = crud.get_user_by_name(db=db, name=value[0])
        country = crud.get_country_by_name(db=db, name=value[4])
        create_review(review=schemas.ReviewCreate(user_id=user.id, country_id=country.id, rating=int(value[2]), remark=value[1], feedback=value[3], review_date=date(*(list(map(int, value[5].split('-')))))), db=db)


