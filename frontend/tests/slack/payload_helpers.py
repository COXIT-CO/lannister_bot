import json


def confirm_button_payload(user):
    return {
        "payload": json.dumps(
            {
                "type": "block_actions",
                "user": {
                    "id": "U03MF8E81T8",
                    "username": user["username"],
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
    }


def modal_payload_on_new_request(*args):
    return {
        "payload": json.dumps(
            {
                "type": "view_submission",
                "team": {"id": "T03MJUGC8HK", "domain": "lannistertestteam"},
                "user": {
                    "id": "U03MF8E81T8",
                    "username": args[0]["username"],
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
                                            "text": args[1]["username"],
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
    }


def edit_request_payload_dropdown(*args):
    print(args)
    return {
        "payload": json.dumps(
            {
                "type": "block_actions",
                "user": {
                    "id": "U03MF8E81T8",
                    "username": args[0]["username"],
                    "name": args[0]["username"],
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
                    "id": args[1]["slack_channel_id"],
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
                                            "text": f"Request id: {args[2]['id']} Created at: 10-07-2022 12:43 EEST, status: Rejected",
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
                                        "text": f"Request id: {args[2]['id']} Created at: 11-07-2022 21:59 EEST, status: Created",
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
                                "text": f"Request id: {args[2]['id']} Created at: 11-07-2022 21:59 EEST, status: Created",
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
    }


def edit_request_modal_payload(*args):
    return {
        "payload": json.dumps(
            {
                "type": "view_submission",
                "team": {"id": "T03MJUGC8HK", "domain": "lannistertestteam"},
                "user": {
                    "id": "U03MF8E81T8",
                    "username": args[0]["username"],
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
                        "text": f"Edit bonus request #{args[1]['id']}",
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
    }


def add_reviewer_payload(*args):
    return {
        "payload": json.dumps(
            {
                "type": "block_actions",
                "user": {
                    "id": "U03MF8E81T8",
                    "username": args[0]["username"],
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
                                        "text": f"id: {args[2]['id']} Overtime by: demigorrgon at 11-07-2022 22:51 EEST",
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
                                        "text": args[1]["username"],
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
    }


def remove_reviewer_payload(*args):
    return {
        "payload": json.dumps(
            {
                "type": "block_actions",
                "user": {
                    "id": "U03MF8E81T8",
                    "username": args[0]["username"],
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
                                        "text": f"Reviewer: {args[1]['username']}, Ka Bob",
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
    }


def history_payload(*args):
    return {
        "payload": json.dumps(
            {
                "type": "block_actions",
                "user": {
                    "id": "U03MF8E81T8",
                    "username": args[0]["username"],
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
                                            "text": f"demigorrgon's Referral request #{args[1]['id']} for $333.00",
                                        },
                                        "value": "value-7",
                                    },
                                    {
                                        "text": {
                                            "type": "plain_text",
                                            "text": f"demigorrgon's Overtime request #{args[1]['id']} for $333.00",
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
                                    "text": f"demigorrgon's Referral request #{args[1]['id']} for $333.00",
                                },
                                "value": "value-7",
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": f"demigorrgon's Overtime request #{args[1]['id']} for $333.00",
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
    }


def approve_button_payload(*args):
    return {
        "payload": json.dumps(
            {
                "type": "block_actions",
                "user": {
                    "id": "U03MF8E81T8",
                    "username": args[0]["username"],
                    "name": "demigorrgon",
                    "team_id": "T03MJUGC8HK",
                },
                "api_app_id": "A03MMSE5XR8",
                "token": "hH0ejgdg1Whg9OMVwRfUKpj8",
                "container": {
                    "type": "message",
                    "message_ts": "1657891516.236209",
                    "channel_id": "D03MK2ADT29",
                },
                "trigger_id": "3804929053554.3732968416597.b6291dfcfc733056d492f2d4f780ea36",
                "team": {"id": "T03MJUGC8HK", "domain": "lannistertestteam"},
                "channel": {"id": "D03MK2ADT29", "name": "directmessage"},
                "message": {
                    "type": "message",
                    "subtype": "bot_message",
                    "text": "This content can't be displayed.",
                    "ts": "1657891516.236209",
                    "username": "lannister-bot",
                    "icons": {"emoji": ":robot_face:"},
                    "bot_id": "B03NBN7SRME",
                    "app_id": "A03MMSE5XR8",
                    "blocks": [
                        {
                            "type": "header",
                            "block_id": "0u=",
                            "text": {
                                "type": "plain_text",
                                "text": "Hey, You! New bonus request to review",
                            },
                        },
                        {"type": "divider", "block_id": "U68mp"},
                        {
                            "type": "section",
                            "block_id": "qHCC",
                            "text": {
                                "type": "mrkdwn",
                                "text": "*demigorrgon has requested the following stuff. Approve or reject it.*",
                            },
                        },
                        {"type": "divider", "block_id": "lZn"},
                        {
                            "type": "section",
                            "block_id": "/NST",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": "Current status: *Created*",
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": "Bonus type: *Referral*",
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": "Requested reward amount: $321.00",
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": "Description: *asdqwe123*",
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": "Requested payment date: *15-07-2022 16:26 EEST*",
                                },
                            ],
                        },
                        {
                            "type": "actions",
                            "block_id": "jAh9U",
                            "elements": [
                                {
                                    "type": "button",
                                    "action_id": f"approve_id_{args[1]['id']}",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Approve",
                                    },
                                    "style": "primary",
                                    "value": "approved_request",
                                },
                                {
                                    "type": "button",
                                    "action_id": f"reject_id_{args[1]['id']}",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Reject",
                                    },
                                    "style": "danger",
                                    "value": "rejected_request",
                                },
                            ],
                        },
                    ],
                },
                "state": {"values": {}},
                "response_url": "https://hooks.slack.com/actions/T03MJUGC8HK/3798319245062/tWgHGp4blTe43drlRy8RunN4",
                "actions": [
                    {
                        "action_id": f"approve_id_{args[1]['id']}",
                        "block_id": "jAh9U",
                        "text": {
                            "type": "plain_text",
                            "text": "Approve",
                        },
                        "value": "approved_request",
                        "style": "primary",
                        "type": "button",
                        "action_ts": "1657891518.787338",
                    }
                ],
            }
        )
    }


def reject_button_payload(*args):
    return {
        "payload": json.dumps(
            {
                "type": "block_actions",
                "user": {
                    "id": "U03MF8E81T8",
                    "username": args[0]["username"],
                    "name": "demigorrgon",
                    "team_id": "T03MJUGC8HK",
                },
                "api_app_id": "A03MMSE5XR8",
                "token": "hH0ejgdg1Whg9OMVwRfUKpj8",
                "container": {
                    "type": "message",
                    "message_ts": "1657891560.821499",
                    "channel_id": "D03MK2ADT29",
                },
                "trigger_id": "3817614556673.3732968416597.a044544e906843931647126343e804f7",
                "team": {"id": "T03MJUGC8HK", "domain": "lannistertestteam"},
                "channel": {"id": "D03MK2ADT29", "name": "directmessage"},
                "message": {
                    "bot_id": "B03NBN7SRME",
                    "type": "message",
                    "text": "reviewer_notification",
                    "user": "U03MQC1M23E",
                    "ts": "1657891560.821499",
                    "app_id": "A03MMSE5XR8",
                    "team": "T03MJUGC8HK",
                    "blocks": [
                        {
                            "type": "header",
                            "block_id": "FUS",
                            "text": {
                                "type": "plain_text",
                                "text": "Deadline of this request is right now. Pls approve or reject:",
                            },
                        },
                        {"type": "divider", "block_id": "3xf"},
                        {
                            "type": "section",
                            "block_id": "BiN",
                            "text": {
                                "type": "mrkdwn",
                                "text": "*demigorrgon has requested the following stuff. Approve or reject it.*",
                            },
                        },
                        {"type": "divider", "block_id": "qYpyd"},
                        {
                            "type": "section",
                            "block_id": "hVT2",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": "Current status: *Created*",
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": "Bonus type: *Referral*",
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": "Requested reward amount: $321.00",
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": "Description: *asdqwe123*",
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": "Requested payment date: *15-07-2022 16:26 EEST*",
                                },
                            ],
                        },
                        {
                            "type": "actions",
                            "block_id": "hub",
                            "elements": [
                                {
                                    "type": "button",
                                    "action_id": "approve_id_56",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Approve",
                                    },
                                    "style": "primary",
                                    "value": "approved_request",
                                },
                                {
                                    "type": "button",
                                    "action_id": "reject_id_56",
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Reject",
                                    },
                                    "style": "danger",
                                    "value": "rejected_request",
                                },
                            ],
                        },
                    ],
                },
                "state": {"values": {}},
                "response_url": "https://hooks.slack.com/actions/T03MJUGC8HK/3828744065760/DhbtUMW6xJMUISK7TR4TfZDn",
                "actions": [
                    {
                        "action_id": f"reject_id_{args[1]['id']}",
                        "block_id": "hub",
                        "text": {
                            "type": "plain_text",
                            "text": "Reject",
                        },
                        "value": "rejected_request",
                        "style": "danger",
                        "type": "button",
                        "action_ts": "1657891993.329571",
                    }
                ],
            },
        )
    }
