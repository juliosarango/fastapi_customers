from sqlmodel import Session, create_engine, SQLModel
from fastapi import Depends, FastAPI
from typing import Annotated

engine = create_engine("sqlite:///db.sqlite3")


def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
