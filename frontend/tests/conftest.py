import pytest
from rest_framework.test import APIClient


@pytest.fixture
def frontend_api_client():
    client = APIClient()
    client.credentials(HTTP_X_SLACK_FRONTEND="slack-frontend-header")
    return client


@pytest.fixture
def api_client_not_registered_in_workspace():
    client = APIClient()
    return client


@pytest.fixture
def admin_user_mock():
    payload = {
        "id": 1,
        "username": "demigorrgon",
        "email": "kabob@gmail.com",
        "first_name": "Some",
        "last_name": "Duud",
        "slack_user_id": "U03MF8E81T8",
        "slack_channel_id": "D03MK2ADT29",
        "roles": [{"name": "Administrator"}, {"name": "Reviewer"}, {"name": "Worker"}],
    }
    return payload


@pytest.fixture
def reviewer_user_mock():
    payload = {
        "id": 3,
        "username": "kabobtest",
        "email": "d@gmail.com",
        "first_name": "Some",
        "last_name": "Idk",
        "slack_user_id": "some123",
        "slack_channel_id": "D03MK2ADT29",
        "roles": [{"name": "Reviewer"}, {"name": "Worker"}],
    }
    return payload


@pytest.fixture
def worker_user_mock():
    payload = {
        "id": 4,
        "username": "kabobtest2",
        "email": "d@gmail.com",
        "first_name": "Some",
        "last_name": "Idk",
        "slack_user_id": "some123",
        "slack_channel_id": "D03MK2ADT29",
        "roles": [{"name": "Worker"}],
    }
    return payload


@pytest.fixture
def bonus_request_mock(worker_user_mock):
    payload = {
        "id": 18,
        "status": "Created",
        "creator": worker_user_mock["username"],
        "reviewer": "demitest",
        "bonus_type": "Referral",
        "description": "asdqwe",
        "created_at": "19-07-2022 23:22 EEST",
        "updated_at": "20-07-2022 12:20 EEST",
        "price_usd": "123.000",
        "payment_date": "20-07-2022 23:23 EEST",
    }

    return payload
