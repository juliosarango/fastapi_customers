from db import SessionDep, create_all_tables
from fastapi import FastAPI, Request
import time

from .routers import customers, transactions, plans

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(plans.router, prefix="/plans", tags=["Plans"])


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.url} completed in: {process_time:.4f} seconds")

    return response
