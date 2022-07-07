import pytest
from django.urls import reverse


pytestmark = [pytest.mark.django_db]

"""
    user_name is default by slack, so pass it like that
    channel_id is your own conversation id with bot, should be valid to receive response in chat
    but pls don't spam my slack channel_id hardcoded here, ty
"""


def test_register_command_api_call_existing_workspace_member_any_role(
    api_client_worker, worker_user
):
    url = reverse("register-in-slack")
    response = api_client_worker.post(
        url,
        {
            "user_name": worker_user.username,
            "channel_id": "D03MK2ADT29",  # hardcoded channel name
        },
    )
    assert response.status_code == 200  # not 201 cuz slack_user_id exists


def test_register_command_api_call_non_workspace_user(
    api_client_not_registered_in_workspace, non_workspace_member
):
    url = reverse("register-in-slack")
    response = api_client_not_registered_in_workspace.post(
        url,
        {
            "user_name": non_workspace_member.username,
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 201


def test_actions_command_api_call_worker_role(api_client_worker, worker_user):
    """
    Response is the same for worker and reviewer
    Admin has to have /list-users, /list-requests
    """
    url = reverse("choose-actions")
    response = api_client_worker.post(
        url, {"user_name": worker_user, "channel_id": "D03MK2ADT29"}
    )
    assert response.status_code == 200


def test_actions_command_by_not_registered_in_workspace_user(
    api_client_not_registered_in_workspace, non_workspace_member
):
    url = reverse("choose-actions")
    response = api_client_not_registered_in_workspace.post(
        url, {"user_name": non_workspace_member.username, "channel_id": "D03MK2ADT29"}
    )
    assert response.status_code == 403


# def test_actions_command_api_call_admin_role(api_client_admin, admin_user):
#     url = reverse("choose-actions")
