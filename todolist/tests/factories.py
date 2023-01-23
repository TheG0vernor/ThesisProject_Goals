import factory

from core.models import User
from goals.models import GoalsCategory, Board, Goals, BoardParticipant


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker(provider='name')
    password = 'test14_16passworD'


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board
    title = 'test_name'


class PartitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalsCategory
    title = 'unq'
    # user = factory.SubFactory(UserFactory)
    # board = factory.SubFactory(BoardFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goals
    title = 'test_names'
    category = factory.SubFactory(CategoryFactory)
    user = factory.SubFactory(UserFactory)
