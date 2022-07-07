import pytest
from mixer.backend.django import mixer
from lannister_auth.models import LannisterUser, Role
from lannister_slack.models import BonusRequest
from rest_framework.test import APIClient


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
    user = LannisterUser.objects.create_user(
        username="Kabob",
        password="someverysecurepass",
        email="k@gmail.com",
        first_name="Abdul",
        last_name="who",
    )
    user.roles.add(admin_role, reviewer_role, worker_role)
    return user


@pytest.fixture
def reviewer_user(reviewer_role, worker_role):
    user = LannisterUser.objects.create_user(
        username="Pleb",
        password="someverysecurepass",
        email="p@gmail.com",
        first_name="gleb",
        last_name="namedpleb",
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
    )
    user.roles.add(worker_role)
    return user


@pytest.fixture()
def superuser():
    return LannisterUser.objects.create_superuser(
        email="demitest@gmail.com",
        username="demitest",
        first_name="kabob",
        last_name="abdul",
        password="hackerman",
    )


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def dummy_bonus_request():
    return mixer.blend(BonusRequest)
