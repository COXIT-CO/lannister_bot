from django.urls import reverse
import pytest

pytestmark = [pytest.mark.django_db]


def test_user_can_register_as_worker(anon_api_client):
    url = reverse("register-user")

    response = anon_api_client.post(
        url,
        {
            "email": "wasda@gmail.com",
            "username": "kabob15",
            "password": "somepassidk",
            "first_name": "ahmud",
            "last_name": "bahmut",
        },
    )

    assert response.status_code == 201
    token_url = reverse("jwt-obtain-token")
    resp = anon_api_client.post(
        token_url,
        {"username": "kabob15", "password": "somepassidk"},
    )
    assert resp.status_code == 200

    anon_api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data.get('access')}")
    user_url = reverse("worker-detail-username", kwargs={"username": "kabob15"})
    user_response = anon_api_client.get(user_url)
    print(user_response.data)
    assert user_response.data.get("roles")[0]["name"] == "Worker"
