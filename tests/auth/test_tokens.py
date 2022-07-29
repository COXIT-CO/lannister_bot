from django.urls import reverse
import pytest

pytestmark = [pytest.mark.django_db]


def test_is_jwt_obtained_on_login(anon_api_client, worker_user):
    url = reverse("jwt-obtain-token")

    response = anon_api_client.post(
        url,
        {
            "username": worker_user.username,
            "password": "someverysecurepass",
        },
    )

    assert response.status_code == 200
    assert response.data.get("access").startswith("e")


def test_provided_wrong_credentials_on_login(anon_api_client, worker_user):
    url = reverse("jwt-obtain-token")

    response = anon_api_client.post(
        url,
        {
            "username": worker_user.username,
            "password": worker_user.password,  # password is hashed in db, supposed to return 401
        },
    )
    assert response.status_code == 401


def test_refresh_token(anon_api_client, worker_user):
    token_url = reverse("jwt-obtain-token")
    token_response = anon_api_client.post(
        token_url,
        {
            "username": worker_user,
            "password": "someverysecurepass",
        },
    )

    url = reverse("jwt-refresh")
    response = anon_api_client.post(
        url, {"refresh": token_response.data.get("refresh")}
    )

    assert response.status_code == 200


def test_verify_token(anon_api_client, reviewer_token):
    url = reverse("jwt-verify")
    response = anon_api_client.post(url, {"token": reviewer_token})

    assert response.status_code == 200
