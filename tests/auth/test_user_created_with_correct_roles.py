import pytest

pytestmark = [pytest.mark.django_db]


def test_create_admin_user(admin_user, admin_role, reviewer_role, worker_role):
    assert admin_role in admin_user.roles.all()
    assert reviewer_role in admin_user.roles.all()
    assert worker_role in admin_user.roles.all()
    assert admin_user.is_superuser is True
    assert admin_user.is_staff is True


def test_create_reviewer_user(reviewer_user, admin_role, reviewer_role, worker_role):
    assert reviewer_role in reviewer_user.roles.all()
    assert worker_role in reviewer_user.roles.all()
    assert admin_role not in reviewer_user.roles.all()


def test_create_worker_user(worker_user, admin_role, reviewer_role, worker_role):
    assert worker_role in worker_user.roles.all()
    assert admin_role not in worker_user.roles.all()
    assert reviewer_role not in worker_user.roles.all()
