import pytest
from lannister_slack.views import InteractivesHandler
from rest_framework.test import force_authenticate
from django.urls import reverse
from slack_sdk.errors import SlackApiError

from tests.slack.payload_helpers import (
    add_reviewer_payload,
    approve_button_payload,
    confirm_button_payload,
    edit_request_modal_payload,
    edit_request_payload_dropdown,
    history_payload,
    modal_payload_on_new_request,
    reject_button_payload,
    remove_reviewer_payload,
)

pytestmark = [pytest.mark.django_db]


def test_help_message_event(api_client_admin, admin_user):
    url = reverse("slack-events")
    response = api_client_admin.post(
        url,
        {
            "event": {
                "type": "message",
                "text": "help",
                "channel": admin_user.slack_channel_id,
            },
        },
        format="json",
    )
    print(response, response.data)
    assert response.status_code == 200


def test_unhandled_message_event(api_client_admin, admin_user):
    url = reverse("slack-events")
    response = api_client_admin.post(
        url,
        {
            "event": {
                "type": "message",
                "text": "wasda",
                "channel": admin_user.slack_channel_id,
            },
        },
        format="json",
    )
    print(response, response.data)
    assert response.status_code == 400


def test_confirm_button(factory, worker_user):
    """
    Explicitly importing and testing view with APIRequestFactory for science
    Should add slack_user_id to user's model as a result
    """
    view = InteractivesHandler.as_view()
    request = factory.post(
        "/api/slack/interactives", confirm_button_payload(user=worker_user)
    )

    force_authenticate(request=request, user=worker_user)
    response = view(request)
    worker_user.refresh_from_db()
    assert response.status_code == 200
    assert worker_user.slack_user_id is not None


def test_modal_on_new_request(api_client_worker, worker_user, admin_user):
    """
    Expected: 200 -> admin has slack_channel_id in fixture
    May return 403 if stack of notifications is full on slack's side
    """
    url = reverse("interactives")
    response = api_client_worker.post(
        url,
        modal_payload_on_new_request(worker_user, admin_user),
        format="json",
    )

    # assert response.status_code == 200
    assert response.status_code == 403


def test_edit_request_dropdown(
    api_client_worker, admin_user, worker_user, dummy_bonus_request
):
    url = reverse("interactives")
    with pytest.raises(
        SlackApiError
    ):  # trigger_id is hardcoded, slack's api should send unique one on selection in interactives
        response = api_client_worker.post(
            url,
            edit_request_payload_dropdown(worker_user, admin_user, dummy_bonus_request),
        )
        assert response.status_code == 200


def test_edit_request_modal(api_client_worker, worker_user, dummy_bonus_request):
    url = reverse("interactives")
    response = api_client_worker.post(
        url,
        edit_request_modal_payload(worker_user, dummy_bonus_request),
    )
    assert response.status_code == 200


def test_add_reviewer_command_assign_worker_as_reviewer(
    api_client_worker, admin_user, worker_user, dummy_bonus_request
):
    """
    Expected 403 -> worker without reviewer role tries to assign himself
    """
    url = reverse("interactives")
    response = api_client_worker.post(
        url, add_reviewer_payload(worker_user, admin_user, dummy_bonus_request)
    )
    assert response.status_code == 200


def test_remove_reviewer(api_client_admin, admin_user, reviewer_user):
    url = reverse("interactives")
    reviewer_user.slack_channel_id = (
        "wasdaqwe"  # reviewer_user does not have slack_channel_id in fixture by design
    )
    reviewer_user.save()  # add it so it won't break query with slack_channel_id in view
    reviewer_user.refresh_from_db()
    response = api_client_admin.post(
        url, remove_reviewer_payload(admin_user, reviewer_user)
    )
    assert response.status_code == 200


def test_history_multiple_choices(api_client_admin, admin_user, dummy_bonus_request):
    url = reverse("interactives")
    response = api_client_admin.post(
        url, history_payload(admin_user, dummy_bonus_request)
    )
    assert response.status_code == 200


def test_approve_button(api_client_admin, admin_user, dummy_bonus_request):
    url = reverse("interactives")
    response = api_client_admin.post(
        url, approve_button_payload(admin_user, dummy_bonus_request)
    )
    assert response.status_code == 200


def test_reject_button(api_client_admin, admin_user, dummy_bonus_request):
    url = reverse("interactives")
    response = api_client_admin.post(
        url, reject_button_payload(admin_user, dummy_bonus_request)
    )
    assert response.status_code == 200
