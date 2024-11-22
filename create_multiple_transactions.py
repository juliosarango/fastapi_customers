from sqlmodel import Session

from db import engine
from models import Customer, Transaction

session = Session(engine)
customer = Customer(
    name="Julio",
    description="Estudiante permanente",
    email="hola@julio.com",
    age=33,
)
session.add(customer)
session.commit()
session.refresh(customer)

for x in range(100):
    session.add(
        Transaction(
            customer_id=customer.id,
            description=f"Test number {x}",
            amount=10 * x,
        )
    )
session.commit()
