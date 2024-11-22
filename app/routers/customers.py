from fastapi import APIRouter, HTTPException, status, Query
from models import (
    Customer,
    CustomerCreate,
    CustomerUpdate,
    Plan,
    CustomerPlan,
    StatusEnum,
)
from db import SessionDep
from sqlmodel import select

router = APIRouter()


@router.post(
    "/",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.get(
    "/",
    response_model=list[Customer],
    status_code=status.HTTP_200_OK,
)
async def get_customers(session: SessionDep):
    return session.exec(select(Customer)).all()


@router.get("/{id}", response_model=Customer)
async def get_customers(id: int, session: SessionDep):
    customer = session.get(Customer, id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    return customer


@router.delete("/{id}")
async def delete_customer(id: int, session: SessionDep):
    customer = session.get(Customer, id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    session.delete(customer)
    session.commit()
    return {"detail": "ok"}


@router.patch(
    "/{id}",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
)
async def update_customer(id: int, customer_data: CustomerUpdate, session: SessionDep):
    customer = session.get(Customer, id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    update_data = customer_data.model_dump(exclude_unset=True)
    customer.sqlmodel_update(update_data)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.post(
    "/{customer_id}/plans/{plan_id}/",
    status_code=status.HTTP_201_CREATED,
)
async def create_customer_plan(
    customer_id: int,
    plan_id: int,
    session: SessionDep,
    plan_status: StatusEnum = Query(),
):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    if not plan_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found",
        )
    customer_plan_db = CustomerPlan(
        customer_id=customer_db.id, plan_id=plan_db.id, status=plan_status
    )
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db


@router.get(
    "/{customer_id}/plans/",
    status_code=status.HTTP_200_OK,
)
async def get_customer_to_plan(
    customer_id: int,
    session: SessionDep,
    plan_status: StatusEnum = Query(),
):
    customer_db = session.get(Customer, customer_id)

    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    query = (
        select(CustomerPlan)
        .where(CustomerPlan.customer_id == customer_id)
        .where(CustomerPlan.status == plan_status)
    )
    plans = session.exec(query).all()

    return plans
