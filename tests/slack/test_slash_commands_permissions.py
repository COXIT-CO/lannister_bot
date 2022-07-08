import pytest
from slack_sdk.errors import SlackApiError
from django.urls import reverse

pytestmark = [pytest.mark.django_db]

"""
    user_name parameter should be passed as first key and this spelling is default by slack, so pass it like that
    channel_id is your own conversation id with bot, should be valid to receive response in chat
    but pls don't spam my slack channel_id hardcoded here, ty
"""

"""
    Tests here are only testing permissions,
    asserting only status codes cuz if anything is provided in Response(data='blahblah'),
    data from Response will show up in user's chat with bot in dictionary/json format on top of slack_client.chat_postMessage call (with block kit elements)
    and data from Response won't be a block kit element and obviously won't have slack's styling applied
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


def test_list_requests_command_api_call_any_role(api_client_reviewer, reviewer_user):
    url = reverse("list-requests")
    response = api_client_reviewer.post(
        url, {"user_name": reviewer_user.username, "channel_id": "D03MK2ADT29"}
    )
    assert response.status_code == 200


def test_list_requests_by_non_workspace_user(
    api_client_not_registered_in_workspace, non_workspace_member
):
    url = reverse("list-requests")
    response = api_client_not_registered_in_workspace.post(
        url, {"user_name": non_workspace_member.username, "channel_id": "D03MK2ADT29"}
    )
    assert response.status_code == 403


def test_new_request_command_api_call_any_role(api_client_worker, worker_user):
    url = reverse("new-request")
    with pytest.raises(SlackApiError) as slack_err:

        response = api_client_worker.post(
            url,
            {
                "user_name": worker_user.username,
                "channel_id": "D03MK2ADT29",
                "trigger_id": "kabob",
            },
        )
        print(response.data)
        assert "failed" in str(slack_err)


def test_new_request_by_non_workspace_user(
    api_client_not_registered_in_workspace, non_workspace_member
):
    url = reverse("new-request")
    # with pytest.raises(SlackApiError):
    response = api_client_not_registered_in_workspace.post(
        url,
        {
            "user_name": non_workspace_member.username,
            "channel_id": "D03MK2ADT29",
            "trigger_id": "kabob",  # modal elements require 'trigger_id'
        },
    )
    assert response.status_code == 403


def test_edit_request_command_api_call_any_role(api_client_reviewer, reviewer_user):
    url = reverse("edit-request")

    response = api_client_reviewer.post(
        url,
        {
            "user_name": reviewer_user.username,
            "channel_id": "D03MK2ADT29",
        },
    )
    print(response.data)
    assert response.status_code == 200


def test_edit_request_by_non_workspace_user(
    api_client_not_registered_in_workspace, non_workspace_member
):
    url = reverse("edit-request")

    response = api_client_not_registered_in_workspace.post(
        url,
        {
            "user_name": non_workspace_member.username,
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 403


def test_review_request_reviewer_role(api_client_reviewer, reviewer_user):
    url = reverse("review-request")
    response = api_client_reviewer.post(
        url,
        {
            "user_name": reviewer_user.username,
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 200


def test_review_request_admin_role(api_client_admin, admin_user):
    url = reverse("review-request")
    response = api_client_admin.post(
        url,
        {
            "user_name": admin_user.username,
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 200  # cuz admin has all the roles by default


def test_review_request_worker_role(api_client_worker, worker_user):
    """
    Test reviewer's permission to review bonus request
    """
    url = reverse("review-request")
    response = api_client_worker.post(
        url,
        {
            "user_name": worker_user.username,
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 403


def test_review_request_non_workspace_member(
    api_client_not_registered_in_workspace, non_workspace_member
):
    url = reverse("review-request")
    response = api_client_not_registered_in_workspace.post(
        url,
        {
            "user_name": non_workspace_member.username,
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 403


def test_add_reviewer_worker_role_with_no_reviewers(api_client_worker, worker_user):
    url = reverse("add-reviewer")
    response = api_client_worker.post(
        url,
        {
            "user_name": worker_user.username,
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 200


def test_add_reviewer_worker_non_workspace_member(
    api_client_not_registered_in_workspace, non_workspace_member
):
    url = reverse("add-reviewer")
    response = api_client_not_registered_in_workspace.post(
        url,
        {
            "user_name": non_workspace_member.username,
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 403


def test_remove_reviewer_role_from_user_by_worker_role(api_client_worker, worker_user):
    url = reverse("remove-reviewer")
    response = api_client_worker.post(
        url,
        {
            "user_name": worker_user.username,
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 403


def test_remove_reviewer_role_from_user_by_admin_role(api_client_admin, admin_user):
    url = reverse("remove-reviewer")
    response = api_client_admin.post(
        url,
        {
            "user_name": admin_user.username,
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 200


def test_remove_reviewer_role_non_workspace_user(
    api_client_not_registered_in_workspace, non_workspace_member
):
    url = reverse("remove-reviewer")
    response = api_client_not_registered_in_workspace.post(
        url,
        {
            "user_name": non_workspace_member.username,
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 403


def test_list_users_any_role(api_client_worker, worker_user):
    url = reverse("list-users")
    response = api_client_worker.post(
        url,
        {
            "user_name": worker_user.username,
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 403


def test_list_users_admin_role(api_client_admin, admin_user):
    url = reverse("list-users")
    response = api_client_admin.post(
        url,
        {
            "user_name": admin_user.username,
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 200


def test_list_users_non_workspace_member(
    api_client_not_registered_in_workspace, non_workspace_member
):
    url = reverse("list-users")
    response = api_client_not_registered_in_workspace.post(
        url,
        {
            "user_name": non_workspace_member.username,
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 403
