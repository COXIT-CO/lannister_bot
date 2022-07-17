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

    user_url = reverse("users-detail", kwargs={"pk": "kabob15"})
    user_response = anon_api_client.get(user_url)
    assert user_response.data.get("roles") == [3]


def test_user_was_registered_by_admin_as_reviewer(api_client_admin):

    url = reverse("register-user")

    api_client_admin
    response = api_client_admin.post(
        url,
        {
            "email": "wasdaqwe@gmail.com",
            "username": "kabob16",
            "password": "somepassidk",
            "first_name": "ahmud",
            "last_name": "bahmut",
        },
    )

    assert response.status_code == 201

    get_user_url = reverse("users-detail", kwargs={"pk": "kabob16"})
    response_single_user = api_client_admin.get(get_user_url)

    # users detail view was found
    assert response_single_user.status_code == 200
    assert response_single_user.data.get("roles") == [2, 3]
