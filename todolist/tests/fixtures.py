import pytest
from rest_framework.test import APIClient

from core.models import User
from tests import factories


@pytest.fixture
def auth_client(user_fixture):
    client = APIClient()
    client.force_authenticate(user_fixture)
    return client


@pytest.fixture
def user_fixture(db):
    user = User.objects.create(
        username='abc2b',
        password='test14_16passworD',
    )
    return user


@pytest.fixture
def category(board, user_fixture):
    return factories.CategoryFactory.create(board=board, user=user_fixture)


@pytest.fixture
def board():
    return factories.BoardFactory.create()


@pytest.fixture
def participant(board, user_fixture):
    participant = factories.PartitionFactory.create(board=board, user=user_fixture)
    return participant


@pytest.fixture
def goal(category, user_fixture):
    return factories.GoalFactory.create(
        title='New_goal',
        category=category,
        user=user_fixture,
        description='описание',
        status=1
    )
