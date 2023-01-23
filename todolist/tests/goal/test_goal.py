import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_create_goal(auth_client, category):
    url = reverse('goal_create')
    expected_response = {
        'title': 'New_goal',
        'category': category.pk
    }
    response = auth_client.post(
        path=url,
        data=expected_response
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_goal2(auth_client, category):
    url = reverse('goal_create')
    expected_response = {
        'title': 'New_goal',
        'category': category.pk
    }
    response = auth_client.post(
        path=url,
        data=expected_response
    )
    response_data = response.json()

    assert response_data.get('category') == expected_response.get('category')


@pytest.mark.django_db
def test_create_goal3(auth_client, category):
    url = reverse('goal_create')
    expected_response = {
        'title': 'New_goal',
        'category': category.pk
    }
    response = auth_client.post(
        path=url,
        data=expected_response
    )
    response_data = response.json()

    assert response_data.get('title') == expected_response.get('title')


@pytest.mark.django_db
def test_create_goal4(auth_client, category):
    url = reverse('goal_create')
    expected_response = {
        'title': 'New_goal',
        'category': category.pk,
        'description': 'описание'
    }
    response = auth_client.post(
        path=url,
        data=expected_response
    )
    response_data = response.json()

    assert response_data.get('description') == expected_response.get('description')


@pytest.mark.django_db
def test_create_goal5(auth_client, category):
    url = reverse('goal_create')
    expected_response = {
        'title': 'New_goal',
        'category': category.pk,
        'status': 1
    }
    response = auth_client.post(
        path=url,
        data=expected_response
    )
    response_data = response.json()

    assert response_data.get('status') == expected_response.get('status')
