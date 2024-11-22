from fastapi import status, HTTPException
import pytest


def test_create_transactions(client):

    response_customer = client.post(
        "/customers",
        json={
            "name": "Prueba",
            "email": "test@test.com",
            "age": 30,
            "description": "Test",
        },
    )

    customer_id = response_customer.json().get("id")

    response_transacction = client.post(
        "/transactions",
        json={"amount": 10, "description": "reclamo", "customer_id": customer_id},
    )
    assert response_transacction.status_code == status.HTTP_201_CREATED
    assert response_transacction.json().get("customer_id") == customer_id


def test_create_transactions_without_customer(client):

    response = client.post(
        "/transactions",
        json={
            "amount": 10,
            "description": "reclamo",
            "customer_id": 20,
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("detail") == "Customer not found"


def test_create_transactions(client):

    response_customer = client.post(
        "/customers",
        json={
            "name": "Prueba",
            "email": "test@test.com",
            "age": 30,
            "description": "Test",
        },
    )

    customer_id = response_customer.json().get("id")

    for x in range(10):
        client.post(
            "/transactions",
            json={
                "amount": 10 * x,
                "description": f"reclamo {x}",
                "customer_id": customer_id,
            },
        )

    response_transactions = client.get(f"/transactions/")
    assert response_transactions.status_code == status.HTTP_200_OK
    assert len(response_transactions.json()) == 10
