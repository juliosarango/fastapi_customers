from pydantic import BaseModel, EmailStr, field_validator
from sqlmodel import SQLModel, Field, Relationship, Session, select
from enum import Enum
from db import engine


class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class CustomerPlan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    plan_id: int = Field(default=None, foreign_key="plan.id")
    customer_id: int = Field(default=None, foreign_key="customer.id")
    status: StatusEnum | None = Field(default=StatusEnum.ACTIVE)


class PlanBase(SQLModel):
    name: str = Field(default=None, max_length=200)
    price: float | None = Field(default=None)
    description: str | None = Field(default=None)


class PlanCreate(PlanBase):
    pass


class Plan(PlanBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customers: list["Customer"] = Relationship(
        back_populates="plans",
        link_model=CustomerPlan,
    )


class CustomerBase(SQLModel):
    name: str = Field(default=None, max_length=200)
    description: str | None = Field(default=None)
    email: EmailStr = Field(default=None)
    age: int = Field(default=None)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        session = Session(engine)
        query = select(Customer).where(Customer.email == value)
        result = session.exec(query).first()
        if result is not None:
            raise ValueError("Email already exists")

        return value


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass


class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list[Plan] = Relationship(
        back_populates="customers",
        link_model=CustomerPlan,
    )


class TransactionBase(SQLModel):
    amount: float
    description: str


class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(default=None, foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="transactions")


class TransactionCreate(TransactionBase):
    customer_id: int = Field(default=None, foreign_key="customer.id")


class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def ammount_total(self):
        return sum([t.amount for t in self.transactions])
