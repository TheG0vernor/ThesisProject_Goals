from pytest_factoryboy import register

from tests.factories import BoardFactory, GoalFactory, CategoryFactory, UserFactory

pytest_plugins = 'tests.fixtures'

register(BoardFactory)
register(GoalFactory)
register(CategoryFactory)
register(UserFactory)
