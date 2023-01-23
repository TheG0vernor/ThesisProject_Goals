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
def test_create_category_goal(auth_client, category):
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
def test_create_title_goal(auth_client, category):
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
def test_create_description_goal(auth_client, category):
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
def test_create_status_goal(auth_client, category):
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


@pytest.mark.django_db
def test_create_priority_goal(auth_client, category):
    url = reverse('goal_create')
    expected_response = {
        'title': 'New_goal',
        'category': category.pk,
        'priority': 2
    }
    response = auth_client.post(
        path=url,
        data=expected_response
    )
    response_data = response.json()

    assert response_data.get('priority') == expected_response.get('priority')


@pytest.mark.django_db
def test_goal_404_httpstatus(auth_client, goal, user_fixture):
    url = reverse('goal', kwargs={'pk': goal.pk})

    response = auth_client.get(path=url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_create_incorrect_priority_goal(auth_client, category):
    url = reverse('goal_create')
    expected_response = {
        'title': 'New_goal',
        'category': category.pk,
        'priority': 5
    }
    response = auth_client.post(
        path=url,
        data=expected_response
    )
    response_data = response.json()

    assert response_data.get('priority') != expected_response.get('priority')

