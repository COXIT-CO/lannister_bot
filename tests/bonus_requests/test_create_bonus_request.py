import pytest
from lannister_slack.models import BonusRequestStatus

pytestmark = [pytest.mark.django_db]


def test_was_signal_to_create_statuses_triggered_on_top_of_created_status_by_mixer(
    dummy_bonus_request,
):
    assert dummy_bonus_request.__class__.objects.values("status") is not None
    assert len(BonusRequestStatus.objects.values("status_name")) == 5
