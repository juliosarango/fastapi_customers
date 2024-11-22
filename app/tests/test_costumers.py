from fastapi import status


def test_create_customer(client):
    response = client.post(
        "/customers",
        json={
            "name": "Prueba",
            "email": "test@test.com",
            "age": 30,
            "description": "Test",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("name") == "Prueba"


def test_read_customer(client):
    response = client.post(
        "/customers",
        json={
            "name": "Prueba",
            "email": "test@test.com",
            "age": 30,
            "description": "Test",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    customer_id: int = response.json().get("id")
    response_read = client.get(f"/customers/{customer_id}")
    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json().get("name") == "Prueba"


def test_read_customer_not_found(client):

    response_read = client.get(f"/customers/123")
    assert response_read.status_code == status.HTTP_404_NOT_FOUND
    assert response_read.json().get("detail") == "Customer not found"


def test_delete_customer_not_found(client):

    response_read = client.delete(f"/customers/123")
    assert response_read.status_code == status.HTTP_404_NOT_FOUND
    assert response_read.json().get("detail") == "Customer not found"


def test_update_customer_not_found(client):

    response_read = client.patch(
        f"/customers/123",
        json={"name": "Prueba2"},
    )
    assert response_read.status_code == status.HTTP_404_NOT_FOUND
    assert response_read.json().get("detail") == "Customer not found"


def test_create_customer_plan_not_found_customer(client):

    response_customer = client.post("/customers/123/plans/123/?plan_status=active")
    assert response_customer.status_code == status.HTTP_404_NOT_FOUND
    assert response_customer.json().get("detail") == "Customer not found"


def test_create_customer_plan_not_found_plan(client):

    customer = client.post(
        "/customers",
        json={
            "name": "Prueba",
            "email": "test@test.com",
            "age": 30,
            "description": "Test",
        },
    )
    customer_id = customer.json().get("id")
    response_customer = client.post(
        f"/customers/{customer_id}/plans/123/?plan_status=active"
    )
    assert response_customer.status_code == status.HTTP_404_NOT_FOUND
    assert response_customer.json().get("detail") == "Plan not found"


def test_read_all_customers(client):
    for x in range(10):
        client.post(
            "/customers",
            json={
                "name": f"Prueba{x}",
                "email": f"test{x}@test.com",
                "age": 30,
                "description": "Test",
            },
        )

    response_read = client.get(f"/customers")
    assert response_read.status_code == status.HTTP_200_OK
    assert len(response_read.json()) == 10


def test_update_customer(client):
    response = client.post(
        "/customers",
        json={
            "name": "Prueba",
            "email": "test@test.com",
            "age": 30,
            "description": "Test",
        },
    )
    customer_id: int = response.json().get("id")

    response_update = client.patch(
        f"/customers/{customer_id}",
        json={
            "name": "Prueba2",
        },
    )

    assert response_update.status_code == status.HTTP_201_CREATED
    assert response_update.json().get("name") == "Prueba2"


def test_create_customer_plan(client):
    response_customer = client.post(
        "/customers",
        json={
            "name": "Prueba",
            "email": "test@test.com",
            "age": 30,
            "description": "Test",
        },
    )
    response_plan = client.post(
        "/plans",
        json={
            "description": "plan basico y gratuito",
            "price": 0,
            "name": "basico",
        },
    )

    customer_id = response_customer.json().get("id")
    plan_id = response_plan.json().get("id")
    response_customer_plan = client.post(
        f"/customers/{customer_id}/plans/{plan_id}/?plan_status=active",
    )

    assert response_customer_plan.status_code == status.HTTP_201_CREATED
    assert response_customer_plan.json().get("status") == "active"

    customer_plans_inactive = client.get(
        f"/customers/{customer_id}/plans/?plan_status=inactive"
    )

    assert customer_plans_inactive.status_code == status.HTTP_200_OK
    assert len(customer_plans_inactive.json()) == 0

    customer_plans_active = client.get(
        f"/customers/{customer_id}/plans/?plan_status=active"
    )
    assert customer_plans_active.status_code == status.HTTP_200_OK
    assert len(customer_plans_active.json()) == 1


def test_delete_customer(client):
    response = client.post(
        "/customers",
        json={
            "name": "Prueba",
            "email": "test@test.com",
            "age": 30,
            "description": "Test",
        },
    )
    customer_id: int = response.json().get("id")
    response_delete = client.delete(f"/customers/{customer_id}")
    assert response_delete.status_code == status.HTTP_200_OK


def test_get_customer_id(client):
    response = client.post(
        "/customers",
        json={
            "name": "Prueba id",
            "email": "test@test.com",
            "age": 30,
            "description": "Test",
        },
    )
    customer_id: int = response.json().get("id")

    response_customer = client.get(f"/customers/{customer_id}")
    assert response_customer.status_code == status.HTTP_200_OK
    assert response_customer.json().get("name") == "Prueba id"


def test_create_customer_plan_without_customer(client):
    customer_plans = client.get("/customers/123/plans/?plan_status=inactive")
    assert customer_plans.status_code == status.HTTP_404_NOT_FOUND
    assert customer_plans.json().get("detail") == "Customer not found"
