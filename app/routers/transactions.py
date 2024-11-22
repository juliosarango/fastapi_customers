from fastapi import APIRouter, HTTPException, status, Query
from models import Transaction, TransactionCreate, Customer
from db import SessionDep
from sqlmodel import select

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_transactions(transaction_data: TransactionCreate, session: SessionDep):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict.get("customer_id"))
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)
    return transaction_db


@router.get("/")
async def get_transactions(
    session: SessionDep,
    skip: int = Query(0, description="Registros a omitir"),
    limit: int = Query(10, description="Número de registros"),
):
    query = select(Transaction).offset(skip).limit(limit)
    return session.exec(query).all()
