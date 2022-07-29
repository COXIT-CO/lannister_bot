from rest_framework.test import APIClient
from django.urls import reverse


def test_workspace_membership_permission_by_slack_api_call(worker_user_mock, mocker):
    random_protected_url = reverse("choose-actions")
    client = APIClient()
    client.credentials(HTTP_USER_AGENT="Slackbot 1.0")
    mocker.patch("requests.get")
    response = client.post(
        random_protected_url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 200
