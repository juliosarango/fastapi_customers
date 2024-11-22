from fastapi import APIRouter, HTTPException, status
from models import Plan, PlanCreate
from db import SessionDep
from sqlmodel import select

router = APIRouter()


@router.post(
    "/",
    response_model=Plan,
    status_code=status.HTTP_201_CREATED,
)
def create_plans(plan_data: PlanCreate, session: SessionDep):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db


@router.get(
    "/",
    response_model=list[Plan],
    status_code=status.HTTP_200_OK,
)
def get_plans(session: SessionDep):
    return session.exec(select(Plan)).all()
