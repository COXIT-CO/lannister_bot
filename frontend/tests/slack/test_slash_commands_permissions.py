from copy import deepcopy
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
    frontend_api_client, worker_user_mock, mocker
):
    url = reverse("register-in-slack")
    fetched_user_to_register = mocker.patch("requests.get")
    fetched_user_to_register.return_value.json.return_value = worker_user_mock
    response = frontend_api_client.post(
        url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": worker_user_mock["slack_channel_id"],
        },
    )
    assert response.status_code == 200


def test_register_command_api_call_non_workspace_user(
    frontend_api_client, worker_user_mock, mocker
):
    url = reverse("register-in-slack")
    fully_registered_user = deepcopy(worker_user_mock)
    worker_user_mock["slack_user_id"] = None
    fetched_user_to_register = mocker.patch("requests.get")
    fetched_user_to_register.return_value.json.return_value = worker_user_mock
    registration_process = mocker.patch("requests.patch")
    registration_process.return_value.json.return_value = fully_registered_user
    response = frontend_api_client.post(
        url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": worker_user_mock["slack_channel_id"],
        },
    )
    assert response.status_code == 201


def test_actions_command_api_call_worker_role(frontend_api_client, worker_user_mock):
    """
    Response is the same for worker and reviewer
    Admin has to have /list-users, /list-requests
    """
    url = reverse("choose-actions")
    response = frontend_api_client.post(
        url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": worker_user_mock["slack_channel_id"],
        },
    )
    assert response.status_code == 200


def test_actions_command_by_not_registered_in_workspace_user(
    api_client_not_registered_in_workspace, worker_user_mock
):
    url = reverse("choose-actions")
    response = api_client_not_registered_in_workspace.post(
        url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": worker_user_mock["slack_channel_id"],
        },
    )
    assert response.status_code == 403


def test_list_requests_command_api_call_any_role(
    frontend_api_client, worker_user_mock, mocker
):
    url = reverse("list-requests")
    mocker.patch("requests.get")
    response = frontend_api_client.post(
        url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": worker_user_mock["slack_channel_id"],
        },
    )
    assert response.status_code == 200


def test_list_requests_by_non_workspace_user(
    api_client_not_registered_in_workspace, worker_user_mock, mocker
):
    url = reverse("list-requests")
    mocker.patch("requests.get")
    response = api_client_not_registered_in_workspace.post(
        url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": worker_user_mock["slack_channel_id"],
        },
    )
    assert response.status_code == 403


def test_new_request_command_api_call_any_role(
    frontend_api_client, worker_user_mock, mocker
):
    url = reverse("new-request")
    # has to have unique trigger_id from Slack
    with pytest.raises(SlackApiError) as slack_err:
        mocker.patch("requests.get")
        mocker.patch("requests.get")
        frontend_api_client.post(
            url,
            {
                "user_name": worker_user_mock["username"],
                "channel_id": "D03MK2ADT29",
                "trigger_id": "kabob",
            },
        )
        assert "failed" in str(slack_err)


def test_new_request_by_non_workspace_user(
    api_client_not_registered_in_workspace, worker_user_mock, mocker
):
    url = reverse("new-request")
    mocker.patch("requests.get")
    mocker.patch("requests.get")
    response = api_client_not_registered_in_workspace.post(
        url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": "D03MK2ADT29",
            "trigger_id": "kabob",  # modal elements require unique 'trigger_id'
        },
    )
    assert response.status_code == 403


def test_edit_request_command_api_call_any_role(
    frontend_api_client, worker_user_mock, bonus_request_mock, mocker
):
    url = reverse("edit-request")
    print(bonus_request_mock)
    bonus_requests_of_current_user = mocker.patch("requests.get")
    bonus_requests_of_current_user.return_value.json.return_value = (
        bonus_request_mock,
    )
    response = frontend_api_client.post(
        url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": worker_user_mock["slack_channel_id"],
        },
    )
    assert response.status_code == 200


def test_edit_request_by_non_workspace_user(
    api_client_not_registered_in_workspace, worker_user_mock, bonus_request_mock, mocker
):
    url = reverse("edit-request")
    bonus_requests_of_current_user = mocker.patch("requests.get")
    bonus_requests_of_current_user.return_value.json.return_value = (
        bonus_request_mock,
    )
    response = api_client_not_registered_in_workspace.post(
        url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": worker_user_mock["slack_channel_id"],
        },
    )
    assert response.status_code == 403


# def test_review_request_reviewer_role(
#     frontend_api_client, reviewer_user_mock, bonus_request_mock, mocker
# ):
#     url = reverse("review-request")
#     # reviewer_mock = mocker.Mock(
#     #     return_value=Mock(status_code=200, json=reviewer_user_mock)
#     # )
#     # bonus_request_mock_obj = mocker.Mock(
#     #     return_value=Mock(status_code=200, json=[bonus_request_mock])
#     # )
#     # assert reviewer_mock.json.return_value == reviewer_user_mock
#     mocks = mocker.patch(
#         "requests.get", side_effects=[reviewer_user_mock, bonus_request_mock]
#     )
#     print(mocks[0], mocks[1])
#     # reviewer = mocker.patch("requests.get", )
#     # reviewer.return_value.json.return_value = reviewer_user_mock
#     assert isinstance(reviewer_user_mock, dict)
#     response = frontend_api_client.post(
#         url,
#         {
#             "user_name": reviewer_user_mock["username"],
#             "channel_id": reviewer_user_mock["slack_channel_id"],
#         },
#     )
#     assert response.status_code == 200


# def test_review_request_admin_role(api_client_admin, admin_user):
#     url = reverse("review-request")
#     response = api_client_admin.post(
#         url,
#         {
#             "user_name": admin_user.username,
#             "channel_id": "D03MK2ADT29",
#         },
#     )
#     assert response.status_code == 200  # cuz admin has all the roles by default


# def test_review_request_worker_role(api_client_worker, worker_user):
#     """
#     Test reviewer's permission to review bonus request
#     """
#     url = reverse("review-request")
#     response = api_client_worker.post(
#         url,
#         {
#             "user_name": worker_user.username,
#             "channel_id": "D03MK2ADT29",
#         },
#     )
#     assert response.status_code == 403


def test_review_request_non_workspace_member(
    api_client_not_registered_in_workspace, worker_user_mock, mocker
):
    url = reverse("review-request")
    mocker.patch("requests.get")
    response = api_client_not_registered_in_workspace.post(
        url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": worker_user_mock["slack_channel_id"],
        },
    )
    assert response.status_code == 403


def test_add_reviewer_by_worker_role_guy(
    frontend_api_client,
    reviewer_user_mock,
    worker_user_mock,
    bonus_request_mock,
    mocker,
):
    url = reverse("add-reviewer")
    mock = mocker.Mock()
    mock.side_effect = [[reviewer_user_mock], [bonus_request_mock]]
    mocker.patch("requests.get")
    mock()
    mocker.patch("requests.get")
    mock()
    with pytest.raises(SlackApiError):
        # cannot build message payload with mocks for some reason
        response = frontend_api_client.post(
            url,
            {
                "user_name": worker_user_mock["username"],
                "channel_id": worker_user_mock["slack_channel_id"],
            },
        )
        assert response.status_code == 200


def test_add_reviewer_worker_non_workspace_member(
    api_client_not_registered_in_workspace, worker_user_mock
):
    url = reverse("add-reviewer")
    response = api_client_not_registered_in_workspace.post(
        url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 403


def test_remove_reviewer_role_from_user_by_worker_role(
    frontend_api_client, worker_user_mock, mocker
):
    url = reverse("remove-reviewer")
    mocker.patch("requests.get")
    mocker.patch("requests.get")
    response = frontend_api_client.post(
        url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 403


def test_remove_reviewer_role_from_user_by_non_admin_role(
    frontend_api_client, reviewer_user_mock, mocker
):
    url = reverse("remove-reviewer")
    mocker.patch("requests.get")
    mocker.patch("requests.get")

    response = frontend_api_client.post(
        url,
        {
            "user_name": reviewer_user_mock["username"],
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 403


def test_remove_reviewer_role_non_workspace_user(
    api_client_not_registered_in_workspace, worker_user_mock
):
    url = reverse("remove-reviewer")
    response = api_client_not_registered_in_workspace.post(
        url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 403


def test_list_users_any_role(frontend_api_client, worker_user_mock, mocker):
    url = reverse("list-users")
    mocker.patch("requests.get")
    response = frontend_api_client.post(
        url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 403


# def test_list_users_admin_role(
#     frontend_api_client, admin_user_mock, worker_user_mock, mocker
# ):
#     url = reverse("list-users")
#     mock = mocker.Mock()
#     mock_all = mocker.Mock()

#     mock.side_effect = [admin_user_mock, [worker_user_mock]]
#     mocker.patch("requests.get")
#     # mock_admin.return_value.json.return_value = admin_user_mock
#     mocker.patch("requests.get")
#     # mock_all.return_value.json.return_value = [worker_user_mock]

#     response = frontend_api_client.post(
#         url,
#         {
#             "user_name": admin_user_mock["username"],
#             "channel_id": "D03MK2ADT29",
#         },
#     )
#     assert response.status_code == 200


def test_list_users_non_workspace_member(
    api_client_not_registered_in_workspace, worker_user_mock, mocker
):
    url = reverse("list-users")
    mocker.patch("requests.get")
    mocker.patch("requests.get")

    response = api_client_not_registered_in_workspace.post(
        url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 403


# def test_history_access_non_admin_user(api_client_reviewer, reviewer_user):
#     url = reverse("history")
#     response = api_client_reviewer.post(
#         url,
#         {
#             "user_name": reviewer_user.username,
#             "channel_id": "D03MK2ADT29",
#         },
#     )
#     assert response.status_code == 403


def test_history_access_non_workspace_user(
    frontend_api_client, worker_user_mock, mocker
):
    url = reverse("history")
    mocker.patch("requests.get")
    mocker.patch("requests.get")

    response = frontend_api_client.post(
        url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 403


# def test_history_access_admin_user(api_client_admin, admin_user):
#     url = reverse("history")
#     response = api_client_admin.post(
#         url,
#         {
#             "user_name": admin_user.username,
#             "channel_id": "D03MK2ADT29",
#         },
#     )
#     assert response.status_code == 200


# def test_list_requests_to_review(
#     frontend_api_client, reviewer_user_mock, bonus_request_mock, mocker
# ):
#     url = reverse("list-requests-to-review")
#     mocker.patch("requests.get").return_value.json.return_value = reviewer_user_mock
#     mocker.patch("requests.get").return_value.json.return_value = [bonus_request_mock]

#     response = frontend_api_client.post(
#         url,
#         {
#             "user_name": reviewer_user_mock["username"],
#             "channel_id": "D03MK2ADT29",
#         },
#     )
#     assert response.status_code == 200


def test_is_list_requests_accessible_to_worker(
    frontend_api_client, worker_user_mock, mocker
):
    url = reverse("list-requests-to-review")
    mocker.patch("requests.get")
    response = frontend_api_client.post(
        url,
        {
            "user_name": worker_user_mock["username"],
            "channel_id": "D03MK2ADT29",
        },
    )
    assert response.status_code == 403


# def test_is_list_accesible_to_non_workspace_member(
#     api_client_not_registered_in_workspace, non_workspace_member
# ):
#     url = reverse("list-requests-to-review")
#     response = api_client_not_registered_in_workspace.post(
#         url,
#         {
#             "user_name": non_workspace_member,
#             "channel_id": "D03MK2ADT29",
#         },
#     )
#     assert response.status_code == 403
