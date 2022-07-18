import pytest
from mixer.backend.django import mixer
from lannister_auth.models import LannisterUser, Role
from lannister_requests.models import (
    BonusRequest,
    BonusRequestStatus,
)
from rest_framework.test import APIClient, APIRequestFactory
from django.urls import reverse


@pytest.fixture
def dummy_user(django_user_model):
    return mixer.blend(django_user_model)


@pytest.fixture
def admin_role():
    return Role.objects.get_or_create(id=1)[0]


@pytest.fixture
def reviewer_role():
    return Role.objects.get_or_create(id=2)[0]


@pytest.fixture
def worker_role():
    return Role.objects.get_or_create(id=3)[0]


@pytest.fixture
def admin_user(admin_role, reviewer_role, worker_role):
    user = LannisterUser.objects.create_superuser(
        username="Kabob",
        password="someverysecurepass",
        email="k@gmail.com",
        first_name="Abdul",
        last_name="who",
    )
    user.roles.add(admin_role, reviewer_role, worker_role)
    user.slack_user_id = "wasdaqwe"
    user.slack_channel_id = "D03MK2ADT29"
    user.save()
    return user


@pytest.fixture
def reviewer_user(reviewer_role, worker_role):
    user = LannisterUser.objects.create_user(
        username="Pleb",
        password="someverysecurepass",
        email="p@gmail.com",
        first_name="gleb",
        last_name="namedpleb",
        slack_user_id="wasdaqwe",
    )
    user.roles.add(reviewer_role, worker_role)
    return user


@pytest.fixture()
def worker_user(worker_role):
    user = LannisterUser.objects.create_user(
        username="stinker",
        password="someverysecurepass",
        email="s@gmail.com",
        first_name="some",
        last_name="idk",
        slack_user_id="wasdaqwe",
    )
    user.roles.add(worker_role)
    return user


@pytest.fixture
def non_workspace_member(worker_role):
    user = LannisterUser.objects.create_user(
        username="stinker",
        password="someverysecurepass",
        email="s@gmail.com",
        first_name="some",
        last_name="idk",
    )
    user.roles.add(worker_role)
    return user


@pytest.fixture
def anon_api_client():
    client = APIClient()
    return client


@pytest.fixture
def admin_token(anon_api_client, admin_user):
    url = reverse("jwt-obtain-token")
    return anon_api_client.post(
        url, {"username": admin_user.username, "password": "someverysecurepass"}
    ).data.get("access")


@pytest.fixture
def reviewer_token(anon_api_client, reviewer_user):
    url = reverse("jwt-obtain-token")
    return anon_api_client.post(
        url, {"username": reviewer_user.username, "password": "someverysecurepass"}
    ).data.get("access")


@pytest.fixture
def worker_token(anon_api_client, worker_user):
    url = reverse("jwt-obtain-token")
    return anon_api_client.post(
        url, {"username": worker_user.username, "password": "someverysecurepass"}
    ).data.get("access")


@pytest.fixture
def non_workspace_member_token(anon_api_client, non_workspace_member):
    url = reverse("jwt-obtain-token")
    return anon_api_client.post(
        url,
        {"username": non_workspace_member.username, "password": "someverysecurepass"},
    ).data.get("access")


@pytest.fixture
def api_client_admin(admin_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    return client


@pytest.fixture
def api_client_reviewer(reviewer_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {reviewer_token}")
    return client


@pytest.fixture
def api_client_worker(worker_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {worker_token}")
    return client


@pytest.fixture
def api_client_not_registered_in_workspace(non_workspace_member_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {non_workspace_member_token}")
    return client


@pytest.fixture
def dummy_status():
    return mixer.blend(BonusRequestStatus)


@pytest.fixture
def dummy_bonus_request():
    return mixer.blend(BonusRequest)


@pytest.fixture
def request_command_mock(mocker):
    mock_slash_register = mocker.patch(
        "lannister_slack.views.SlackEventView",
    )
    mock_slash_register.return_value.data = {
        "team_id": "T03MJUGC8HK",  #
        "channel_name": "directmessage",
        "command": "/register",
    }
    return mock_slash_register.return_value.data


@pytest.fixture
def factory():
    factory = APIRequestFactory()
    return factory
