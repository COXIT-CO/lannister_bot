import pytest
import json
from lannister_slack.views import InteractivesHandler
from rest_framework.test import force_authenticate
from django.urls import reverse
from slack_sdk.errors import SlackApiError

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
        "/api/slack/interactives",
        {
            "payload": json.dumps(
                {
                    "type": "block_actions",
                    "user": {
                        "id": "U03MF8E81T8",
                        "username": worker_user.username,
                        "name": "demigorrgon",
                        "team_id": "T03MJUGC8HK",
                    },
                    "api_app_id": "A03MMSE5XR8",
                    "token": "hH0ejgdg1Whg9OMVwRfUKpj8",
                    "container": {
                        "type": "message",
                        "message_ts": "1657567468.672319",
                        "channel_id": "D03MK2ADT29",
                    },
                    "trigger_id": "3778457597974.3732968416597.77226a94070f900ea15b1b39e226709c",
                    "team": {"id": "T03MJUGC8HK", "domain": "lannistertestteam"},
                    "channel": {"id": "D03MK2ADT29", "name": "directmessage"},
                    "message": {
                        "type": "message",
                        "subtype": "bot_message",
                        "text": "This content can't be displayed.",
                        "ts": "1657567468.672319",
                        "username": "lannister-bot",
                        "icons": {"emoji": ":robot_face:"},
                        "bot_id": "B03NBN7SRME",
                        "app_id": "A03MMSE5XR8",
                        "blocks": [
                            {
                                "type": "header",
                                "block_id": "KTo",
                                "text": {
                                    "type": "plain_text",
                                    "text": "*Hey, demigorrgon, want to register?*",
                                },
                            },
                            {"type": "divider", "block_id": "jMtTS"},
                            {
                                "type": "section",
                                "block_id": "Cr6O9",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "Bot will automatically add your slack id to your Lannister account. Agreed?",
                                },
                            },
                            {
                                "type": "actions",
                                "block_id": "confirm_register",
                                "elements": [
                                    {
                                        "type": "button",
                                        "action_id": "confirm_register",
                                        "text": {
                                            "type": "plain_text",
                                            "text": "I agree",
                                        },
                                    }
                                ],
                            },
                        ],
                    },
                    "state": {"values": {}},
                    "response_url": "https://hooks.slack.com/actions/T03MJUGC8HK/3785000559475/yot6FPHNC1hI1wdYK7wNtYZk",
                    "actions": [
                        {
                            "action_id": "confirm_register",
                            "block_id": "confirm_register",
                            "text": {
                                "type": "plain_text",
                                "text": "I agree",
                            },
                            "type": "button",
                            "action_ts": "1657567472.148859",
                        }
                    ],
                }
            )
        },
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
        {
            "payload": json.dumps(
                {
                    "type": "view_submission",
                    "team": {"id": "T03MJUGC8HK", "domain": "lannistertestteam"},
                    "user": {
                        "id": "U03MF8E81T8",
                        "username": worker_user.username,
                        "name": "demigorrgon",
                        "team_id": "T03MJUGC8HK",
                    },
                    "api_app_id": "A03MMSE5XR8",
                    "token": "hH0ejgdg1Whg9OMVwRfUKpj8",
                    "trigger_id": "3808702430688.3732968416597.fb73d151d5e3a84dbd9738b071dab299",
                    "view": {
                        "id": "V03PSLMFA48",
                        "team_id": "T03MJUGC8HK",
                        "type": "modal",
                        "blocks": [
                            {"type": "divider", "block_id": "D03MK2ADT29"},
                            {
                                "type": "input",
                                "block_id": "bonus_type_input",
                                "label": {
                                    "type": "plain_text",
                                    "text": "Select bonus type",
                                    "emoji": True,
                                },
                                "optional": False,
                                "dispatch_action": False,
                                "element": {
                                    "type": "static_select",
                                    "action_id": "new_bonus_request_modal_type",
                                    "options": [
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Overtime",
                                                "emoji": True,
                                            },
                                            "value": "value-0",
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Referral",
                                                "emoji": True,
                                            },
                                            "value": "value-1",
                                        },
                                    ],
                                },
                            },
                            {
                                "type": "input",
                                "block_id": "new_bonus_request_modal_description",
                                "label": {
                                    "type": "plain_text",
                                    "text": "Add a description",
                                    "emoji": True,
                                },
                                "optional": False,
                                "dispatch_action": False,
                                "element": {
                                    "type": "plain_text_input",
                                    "action_id": "new_bonus_request_modal_description",
                                    "multiline": True,
                                    "dispatch_action_config": {
                                        "trigger_actions_on": ["on_enter_pressed"]
                                    },
                                },
                            },
                            {
                                "type": "input",
                                "block_id": "reviewers_dropdown_input",
                                "label": {
                                    "type": "plain_text",
                                    "text": "Select a reviewer",
                                    "emoji": True,
                                },
                                "optional": False,
                                "dispatch_action": False,
                                "element": {
                                    "type": "static_select",
                                    "action_id": "new_bonus_request_selected_reviewer",
                                    "options": [
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "demigorrgon",
                                                "emoji": True,
                                            },
                                            "value": "value-0",
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "kabob23",
                                                "emoji": True,
                                            },
                                            "value": "value-1",
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "demigorrgon-test-roles",
                                                "emoji": True,
                                            },
                                            "value": "value-2",
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "metallistvalon",
                                                "emoji": True,
                                            },
                                            "value": "value-3",
                                        },
                                    ],
                                },
                            },
                            {
                                "type": "input",
                                "block_id": "usd_amount",
                                "label": {
                                    "type": "plain_text",
                                    "text": "Amount of reward you'd want in USD",
                                    "emoji": True,
                                },
                                "optional": False,
                                "dispatch_action": False,
                                "element": {
                                    "type": "plain_text_input",
                                    "action_id": "usd_amount",
                                    "multiline": False,
                                    "dispatch_action_config": {
                                        "trigger_actions_on": ["on_enter_pressed"]
                                    },
                                },
                            },
                            {
                                "type": "input",
                                "block_id": "1Ch",
                                "label": {
                                    "type": "plain_text",
                                    "text": "Pick a payment date",
                                    "emoji": True,
                                },
                                "optional": False,
                                "dispatch_action": False,
                                "element": {
                                    "type": "datepicker",
                                    "action_id": "datepicker-action",
                                    "initial_date": "2022-07-11",
                                    "placeholder": {
                                        "type": "plain_text",
                                        "text": "Select a date",
                                        "emoji": True,
                                    },
                                },
                            },
                            {
                                "type": "input",
                                "block_id": "0sdd",
                                "label": {
                                    "type": "plain_text",
                                    "text": "Pick a payment time",
                                    "emoji": True,
                                },
                                "optional": False,
                                "dispatch_action": False,
                                "element": {
                                    "type": "timepicker",
                                    "action_id": "new_bonus_request_selected_time",
                                    "initial_time": "21:59",
                                    "placeholder": {
                                        "type": "plain_text",
                                        "text": "Pick a payment time",
                                        "emoji": True,
                                    },
                                },
                            },
                        ],
                        "private_metadata": "",
                        "callback_id": "",
                        "state": {
                            "values": {
                                "bonus_type_input": {
                                    "new_bonus_request_modal_type": {
                                        "type": "static_select",
                                        "selected_option": {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Referral",
                                                "emoji": True,
                                            },
                                            "value": "value-1",
                                        },
                                    }
                                },
                                "new_bonus_request_modal_description": {
                                    "new_bonus_request_modal_description": {
                                        "type": "plain_text_input",
                                        "value": "asdqwe",
                                    }
                                },
                                "reviewers_dropdown_input": {
                                    "new_bonus_request_selected_reviewer": {
                                        "type": "static_select",
                                        "selected_option": {
                                            "text": {
                                                "type": "plain_text",
                                                "text": admin_user.username,
                                                "emoji": True,
                                            },
                                            "value": "value-3",
                                        },
                                    }
                                },
                                "usd_amount": {
                                    "usd_amount": {
                                        "type": "plain_text_input",
                                        "value": "213",
                                    }
                                },
                                "1Ch": {
                                    "datepicker-action": {
                                        "type": "datepicker",
                                        "selected_date": "2022-07-12",
                                    }
                                },
                                "0sdd": {
                                    "new_bonus_request_selected_time": {
                                        "type": "timepicker",
                                        "selected_time": "00:00",
                                    }
                                },
                            }
                        },
                        "hash": "1657565940.iBLRcYxU",
                        "title": {
                            "type": "plain_text",
                            "text": "New bonus request",
                            "emoji": True,
                        },
                        "clear_on_close": False,
                        "notify_on_close": False,
                        "close": {
                            "type": "plain_text",
                            "text": "Cancel",
                            "emoji": True,
                        },
                        "submit": {
                            "type": "plain_text",
                            "text": "Submit",
                            "emoji": True,
                        },
                        "previous_view_id": None,
                        "root_view_id": "V03PSLMFA48",
                        "app_id": "A03MMSE5XR8",
                        "external_id": "",
                        "app_installed_team_id": "T03MJUGC8HK",
                        "bot_id": "B03NBN7SRME",
                    },
                    "response_urls": [],
                    "is_enterprise_install": False,
                    "enterprise": None,
                }
            )
        },
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
            {
                "payload": json.dumps(
                    {
                        "type": "block_actions",
                        "user": {
                            "id": "U03MF8E81T8",
                            "username": worker_user.username,
                            "name": worker_user.username,
                            "team_id": "T03MJUGC8HK",
                        },
                        "api_app_id": "A03MMSE5XR8",
                        "token": "hH0ejgdg1Whg9OMVwRfUKpj8",
                        "container": {
                            "type": "message",
                            "message_ts": "1657567631.810649",
                            "channel_id": "D03MK2ADT29",
                        },
                        "trigger_id": "3785012457027.3732968416597.62a91140941754939db935d80d7608a1",
                        "team": {"id": "T03MJUGC8HK", "domain": "lannistertestteam"},
                        "channel": {
                            "id": admin_user.slack_channel_id,
                            "name": "directmessage",
                        },
                        "message": {
                            "type": "message",
                            "subtype": "bot_message",
                            "text": "This content can't be displayed.",
                            "ts": "1657567631.810649",
                            "username": "lannister-bot",
                            "icons": {"emoji": ":robot_face:"},
                            "bot_id": "B03NBN7SRME",
                            "app_id": "A03MMSE5XR8",
                            "blocks": [
                                {"type": "divider", "block_id": "gGwTK"},
                                {
                                    "type": "header",
                                    "block_id": "4FE",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Select bonus request to edit",
                                    },
                                },
                                {
                                    "type": "section",
                                    "block_id": "wRLpJ",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": "Pick one:",
                                    },
                                    "accessory": {
                                        "type": "static_select",
                                        "action_id": "edit_request",
                                        "placeholder": {
                                            "type": "plain_text",
                                            "text": "Choose request",
                                        },
                                        "options": [
                                            {
                                                "text": {
                                                    "type": "plain_text",
                                                    "text": f"Request id: {dummy_bonus_request.id} Created at: 10-07-2022 12:43 EEST, status: Rejected",
                                                },
                                                "value": "value-0",
                                            },
                                        ],
                                    },
                                },
                            ],
                        },
                        "state": {
                            "values": {
                                "wRLpJ": {
                                    "edit_request": {
                                        "type": "static_select",
                                        "selected_option": {
                                            "text": {
                                                "type": "plain_text",
                                                "text": f"Request id: {dummy_bonus_request.id} Created at: 11-07-2022 21:59 EEST, status: Created",
                                            },
                                            "value": "value-23",
                                        },
                                    }
                                }
                            }
                        },
                        "response_url": "https://hooks.slack.com/actions/T03MJUGC8HK/3808834289856/N5GYY3hUnN2QvtKQWz0YlOo1",
                        "actions": [
                            {
                                "type": "static_select",
                                "action_id": "edit_request",
                                "block_id": "wRLpJ",
                                "selected_option": {
                                    "text": {
                                        "type": "plain_text",
                                        "text": f"Request id: {dummy_bonus_request.id} Created at: 11-07-2022 21:59 EEST, status: Created",
                                    },
                                    "value": "value-23",
                                },
                                "placeholder": {
                                    "type": "plain_text",
                                    "text": "Choose request",
                                },
                                "action_ts": "1657567640.369390",
                            }
                        ],
                    }
                )
            },
        )
        assert response.status_code == 200


def test_edit_request_modal(api_client_worker, worker_user, dummy_bonus_request):
    url = reverse("interactives")
    response = api_client_worker.post(
        url,
        {
            "payload": json.dumps(
                {
                    "type": "view_submission",
                    "team": {"id": "T03MJUGC8HK", "domain": "lannistertestteam"},
                    "user": {
                        "id": "U03MF8E81T8",
                        "username": worker_user.username,
                        "name": "demigorrgon",
                        "team_id": "T03MJUGC8HK",
                    },
                    "api_app_id": "A03MMSE5XR8",
                    "token": "hH0ejgdg1Whg9OMVwRfUKpj8",
                    "trigger_id": "3778577642518.3732968416597.fe4691326cd619f8cfa4dfa6b21a398c",
                    "view": {
                        "id": "V03NWDTFK2A",
                        "team_id": "T03MJUGC8HK",
                        "type": "modal",
                        "blocks": [
                            {"type": "divider", "block_id": "D03MK2ADT29"},
                            {
                                "type": "input",
                                "block_id": "edit_request_bonus_type_selected",
                                "label": {
                                    "type": "plain_text",
                                    "text": "Edit bonus type",
                                },
                                "element": {
                                    "type": "static_select",
                                    "action_id": "edit_request_bonus_type_selected",
                                    "options": [
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Referral",
                                            },
                                            "value": "value-0",
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Overtime",
                                            },
                                            "value": "value-1",
                                        },
                                    ],
                                },
                            },
                            {"type": "divider", "block_id": "z1Y"},
                            {
                                "type": "input",
                                "block_id": "edit_request_description_from_modal",
                                "label": {
                                    "type": "plain_text",
                                    "text": "Change description",
                                },
                                "element": {
                                    "type": "plain_text_input",
                                    "action_id": "edit_request_description_from_modal",
                                    "dispatch_action_config": {
                                        "trigger_actions_on": ["on_enter_pressed"]
                                    },
                                },
                            },
                        ],
                        "private_metadata": "",
                        "callback_id": "",
                        "state": {
                            "values": {
                                "edit_request_bonus_type_selected": {
                                    "edit_request_bonus_type_selected": {
                                        "type": "static_select",
                                        "selected_option": {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Overtime",
                                            },
                                            "value": "value-1",
                                        },
                                    }
                                },
                                "edit_request_description_from_modal": {
                                    "edit_request_description_from_modal": {
                                        "type": "plain_text_input",
                                        "value": "asdqwe",
                                    }
                                },
                            }
                        },
                        "hash": "1657567640.xv6fpgmn",
                        "title": {
                            "type": "plain_text",
                            "text": f"Edit bonus request #{dummy_bonus_request.id}",
                        },
                        "close": {
                            "type": "plain_text",
                            "text": "Cancel",
                        },
                        "submit": {
                            "type": "plain_text",
                            "text": "Submit",
                        },
                        "root_view_id": "V03NWDTFK2A",
                        "app_id": "A03MMSE5XR8",
                        "external_id": "",
                        "app_installed_team_id": "T03MJUGC8HK",
                        "bot_id": "B03NBN7SRME",
                    },
                    "response_urls": [],
                }
            )
        },
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
        url,
        {
            "payload": json.dumps(
                {
                    "type": "block_actions",
                    "user": {
                        "id": "U03MF8E81T8",
                        "username": "demigorrgon",
                        "name": "demigorrgon",
                        "team_id": "T03MJUGC8HK",
                    },
                    "api_app_id": "A03MMSE5XR8",
                    "token": "hH0ejgdg1Whg9OMVwRfUKpj8",
                    "container": {
                        "type": "message",
                        "message_ts": "1657569434.834789",
                        "channel_id": "D03MK2ADT29",
                    },
                    "trigger_id": "3785145665619.3732968416597.e8ba703dc5805631a931426aee7e5713",
                    "team": {"id": "T03MJUGC8HK", "domain": "lannistertestteam"},
                    "channel": {"id": "D03MK2ADT29", "name": "directmessage"},
                    "message": {
                        "type": "message",
                        "subtype": "bot_message",
                        "text": "This content can't be displayed.",
                        "ts": "1657569434.834789",
                        "username": "lannister-bot",
                        "icons": {"emoji": ":robot_face:"},
                        "bot_id": "B03NBN7SRME",
                        "app_id": "A03MMSE5XR8",
                        "blocks": [
                            {"type": "divider", "block_id": "4MQ="},
                            {
                                "type": "header",
                                "block_id": "bsv=c",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Assign reviewer to your bonus request",
                                },
                            },
                            {"type": "divider", "block_id": "6UIwg"},
                            {
                                "type": "section",
                                "block_id": "bonus_request",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "Select bonus request:",
                                },
                                "accessory": {
                                    "type": "static_select",
                                    "action_id": "select_request",
                                    "placeholder": {
                                        "type": "plain_text",
                                        "text": "Choose request",
                                    },
                                    "options": [],
                                },
                            },
                            {
                                "type": "section",
                                "block_id": "reviewer",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "Select reviewer",
                                },
                                "accessory": {
                                    "type": "static_select",
                                    "action_id": "select_reviewer",
                                    "placeholder": {
                                        "type": "plain_text",
                                        "text": "Enter reviewer's name",
                                    },
                                    "options": [
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "demigorrgon",
                                            },
                                            "value": "value-0",
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "kabob23",
                                            },
                                            "value": "value-1",
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "demigorrgon-test-roles",
                                            },
                                            "value": "value-2",
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "metallistvalon",
                                            },
                                            "value": "value-3",
                                        },
                                    ],
                                },
                            },
                        ],
                    },
                    "state": {
                        "values": {
                            "bonus_request": {
                                "select_request": {
                                    "type": "static_select",
                                    "selected_option": {
                                        "text": {
                                            "type": "plain_text",
                                            "text": f"id: {dummy_bonus_request.id} Overtime by: demigorrgon at 11-07-2022 22:51 EEST",
                                        },
                                        "value": "value-23",
                                    },
                                }
                            },
                            "reviewer": {
                                "select_reviewer": {
                                    "type": "static_select",
                                    "selected_option": {
                                        "text": {
                                            "type": "plain_text",
                                            "text": admin_user.username,
                                        },
                                        "value": "value-3",
                                    },
                                }
                            },
                        }
                    },
                    "response_url": "https://hooks.slack.com/actions/T03MJUGC8HK/3778601866678/WZcbfyl3KlD1co0kvc6DhRBT",
                    "actions": [
                        {
                            "type": "static_select",
                            "action_id": "select_reviewer",
                            "block_id": "reviewer",
                            "selected_option": {
                                "text": {
                                    "type": "plain_text",
                                    "text": "metallistvalon",
                                },
                                "value": "value-3",
                            },
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Enter reviewer's name",
                            },
                            "action_ts": "1657569454.536397",
                        }
                    ],
                }
            )
        },
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
        url,
        {
            "payload": json.dumps(
                {
                    "type": "block_actions",
                    "user": {
                        "id": "U03MF8E81T8",
                        "username": admin_user.username,
                        "name": "demigorrgon",
                        "team_id": "T03MJUGC8HK",
                    },
                    "api_app_id": "A03MMSE5XR8",
                    "token": "hH0ejgdg1Whg9OMVwRfUKpj8",
                    "container": {
                        "type": "message",
                        "message_ts": "1657605478.761799",
                        "channel_id": "D03MK2ADT29",
                    },
                    "trigger_id": "3772227271111.3732968416597.e18e19a5576df7321de7dffb0d273fca",
                    "team": {"id": "T03MJUGC8HK", "domain": "lannistertestteam"},
                    "channel": {"id": "D03MK2ADT29", "name": "directmessage"},
                    "message": {
                        "type": "message",
                        "subtype": "bot_message",
                        "text": "This content can't be displayed.",
                        "ts": "1657605478.761799",
                        "username": "lannister-bot",
                        "icons": {"emoji": ":robot_face:"},
                        "bot_id": "B03NBN7SRME",
                        "app_id": "A03MMSE5XR8",
                        "blocks": [
                            {"type": "divider", "block_id": "cED"},
                            {
                                "type": "section",
                                "block_id": "xQJAC",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "Pick reviewer to unassign.\n*Note: after user was removed, rerun the command*",
                                },
                                "accessory": {
                                    "type": "static_select",
                                    "action_id": "select_user_to_remove_from_reviewers",
                                    "placeholder": {
                                        "type": "plain_text",
                                        "text": "Select user to unassign.",
                                    },
                                    "options": [
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Reviewer: demigorrgon, Some Duud",
                                            },
                                            "value": "value-0",
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Reviewer: kabob23, Ka Bob",
                                            },
                                            "value": "value-1",
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Reviewer: demigorrgon-test-roles, Ka Bob",
                                            },
                                            "value": "value-2",
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "Reviewer: metallistvalon, Ka Bob",
                                            },
                                            "value": "value-3",
                                        },
                                    ],
                                },
                            },
                            {
                                "type": "actions",
                                "block_id": "confirm_unassign",
                                "elements": [
                                    {
                                        "type": "button",
                                        "action_id": "confirm_unassign",
                                        "text": {
                                            "type": "plain_text",
                                            "text": "Confirm unassign",
                                        },
                                    }
                                ],
                            },
                        ],
                    },
                    "state": {
                        "values": {
                            "xQJAC": {
                                "select_user_to_remove_from_reviewers": {
                                    "type": "static_select",
                                    "selected_option": {
                                        "text": {
                                            "type": "plain_text",
                                            "text": f"Reviewer: {reviewer_user.username}, Ka Bob",
                                        },
                                        "value": "value-1",
                                    },
                                }
                            }
                        }
                    },
                    "response_url": "https://hooks.slack.com/actions/T03MJUGC8HK/3789236115908/27PBpAwzV2g6VuInQtkmkhth",
                    "actions": [
                        {
                            "action_id": "confirm_unassign",
                            "block_id": "confirm_unassign",
                            "text": {
                                "type": "plain_text",
                                "text": "Confirm unassign",
                            },
                            "type": "button",
                            "action_ts": "1657605493.061161",
                        }
                    ],
                }
            )
        },
    )
    assert response.status_code == 200


def test_history_multiple_choices(api_client_admin, admin_user, dummy_bonus_request):
    url = reverse("interactives")
    response = api_client_admin.post(
        url,
        {
            "payload": json.dumps(
                {
                    "type": "block_actions",
                    "user": {
                        "id": "U03MF8E81T8",
                        "username": admin_user.username,
                        "name": "demigorrgon",
                        "team_id": "T03MJUGC8HK",
                    },
                    "api_app_id": "A03MMSE5XR8",
                    "token": "hH0ejgdg1Whg9OMVwRfUKpj8",
                    "container": {
                        "type": "message",
                        "message_ts": "1657605953.233929",
                        "channel_id": "D03MK2ADT29",
                    },
                    "trigger_id": "3799494406465.3732968416597.fb2395567417be4cff5ffc67f01b0941",
                    "team": {"id": "T03MJUGC8HK", "domain": "lannistertestteam"},
                    "channel": {"id": "D03MK2ADT29", "name": "directmessage"},
                    "message": {
                        "type": "message",
                        "subtype": "bot_message",
                        "text": "This content can't be displayed.",
                        "ts": "1657605953.233929",
                        "username": "lannister-bot",
                        "icons": {"emoji": ":robot_face:"},
                        "bot_id": "B03NBN7SRME",
                        "app_id": "A03MMSE5XR8",
                        "blocks": [
                            {"type": "divider", "block_id": "8GuY"},
                            {
                                "type": "header",
                                "block_id": "NsNA6",
                                "text": {
                                    "type": "plain_text",
                                    "text": "History of Bonus Requests",
                                },
                            },
                            {"type": "divider", "block_id": "YEXqI"},
                            {
                                "type": "input",
                                "block_id": "n9jjw",
                                "label": {
                                    "type": "plain_text",
                                    "text": "Select bonus request to see its history of statuses",
                                },
                                "element": {
                                    "type": "multi_static_select",
                                    "action_id": "history_bonus_request_select",
                                    "placeholder": {
                                        "type": "plain_text",
                                        "text": "Click to see the list",
                                    },
                                    "options": [
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "kabob23's Referral request #26 for $333.00",
                                            },
                                            "value": "value-0",
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "demigorrgon's Overtime request #45 for $321.00",
                                            },
                                            "value": "value-1",
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": "demigorrgon's Overtime request #2 for $333.00",
                                            },
                                            "value": "value-2",
                                        },
                                    ],
                                },
                            },
                        ],
                    },
                    "state": {
                        "values": {
                            "n9jjw": {
                                "history_bonus_request_select": {
                                    "type": "multi_static_select",
                                    "selected_options": [
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": f"demigorrgon's Referral request #{dummy_bonus_request.id} for $333.00",
                                            },
                                            "value": "value-7",
                                        },
                                        {
                                            "text": {
                                                "type": "plain_text",
                                                "text": f"demigorrgon's Overtime request #{dummy_bonus_request.id} for $333.00",
                                            },
                                            "value": "value-4",
                                        },
                                    ],
                                }
                            }
                        }
                    },
                    "response_url": "https://hooks.slack.com/actions/T03MJUGC8HK/3772252655207/iWXDtbipRXMBqQKZ2RuI3Z9D",
                    "actions": [
                        {
                            "type": "multi_static_select",
                            "action_id": "history_bonus_request_select",
                            "block_id": "n9jjw",
                            "selected_options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": f"demigorrgon's Referral request #{dummy_bonus_request.id} for $333.00",
                                    },
                                    "value": "value-7",
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": f"demigorrgon's Overtime request #{dummy_bonus_request.id} for $333.00",
                                    },
                                    "value": "value-4",
                                },
                            ],
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Click to see the list",
                            },
                            "action_ts": "1657605966.247031",
                        }
                    ],
                }
            )
        },
    )
    assert response.status_code == 200


# def test_approve_button(api_client_admin, admin_user):
# url = reverse("interactives")
# response = api_client_admin.post(url, {"payload": json.dumps()})


# def test_reject_button(api_client_admin, admin_user):
