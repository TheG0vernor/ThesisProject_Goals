import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_create_goal(auth_client, category):
    url = reverse('goal_create')
    expected_response = {
        'title': 'Newgoal',
        'category': category.pk
    }
    response = auth_client.post(
        path=url,
        data=expected_response
    )
    response = response.json()
    assert response.status_code == status.HTTP_201_CREATED