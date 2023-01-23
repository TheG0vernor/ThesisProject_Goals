from pytest_factoryboy import register

from tests.factories import BoardFactory, GoalFactory, CategoryFactory, UserFactory, PartitionFactory

pytest_plugins = 'tests.fixtures'

register(BoardFactory)
register(GoalFactory)
register(CategoryFactory)
register(PartitionFactory)
register(UserFactory)
