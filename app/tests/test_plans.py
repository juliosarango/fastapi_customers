from fastapi import status


def test_create_plan(client):
    response = client.post(
        "/plans",
        json={
            "description": "plan basico y gratuito",
            "price": 0,
            "name": "basico",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("name") == "basico"


def test_get_plans(client):

    for x in range(10):
        client.post(
            "/plans",
            json={
                "description": "plan basico y gratuito",
                "price": 0,
                "name": "basico",
            },
        )

    response_read = client.get("/plans")
    assert response_read.status_code == status.HTTP_200_OK
    assert len(response_read.json()) == 10
