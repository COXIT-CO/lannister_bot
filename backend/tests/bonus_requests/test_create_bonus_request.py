import pytest
from lannister_requests.models import BonusRequestsHistory

pytestmark = [pytest.mark.django_db]


# def test_bonus_request_created(dummy_bonus_request):
#     assert isinstance(dummy_bonus_request.id, int)


def test_status_created(dummy_status):
    assert isinstance(dummy_status.id, int)


# def test_history_model_created_on_bonus_request_creation(dummy_bonus_request):
#     assert isinstance(dummy_bonus_request.id, int)
#     assert BonusRequestsHistory.objects.all().count() == 1
