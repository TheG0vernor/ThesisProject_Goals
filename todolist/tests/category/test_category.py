import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_create_category(auth_client, board):
    url = reverse('category_create')
    expected_response = {
        'title': 'unq',
        'board': board.pk
    }
    response = auth_client.post(
        path=url,
        data=expected_response
    )
    response_data = response.json()

    assert response_data.get('title') == expected_response.get('title')


@pytest.mark.django_db
def test_create_status_category(auth_client, board):
    url = reverse('category_create')
    expected_response = {
        'title': 'unq',
        'board': board.pk
    }
    response = auth_client.post(
        path=url,
        data=expected_response
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_is_deleted_hide_category(auth_client, board):
    url = reverse('category_create')
    expected_response = {
        'title': 'unq',
        'board': board.pk
    }
    response = auth_client.post(
        path=url,
        data=expected_response
    )

    response_data = response.json()

    assert response_data.get('is_deleted') is False


@pytest.mark.django_db
def test_create_is_deleted_category(auth_client, board):
    url = reverse('category_create')
    expected_response = {
        'title': 'unq',
        'board': board.pk,
        'is_deleted': True
    }
    response = auth_client.post(
        path=url,
        data=expected_response
    )

    response_data = response.json()

    assert response_data.get('is_deleted') is True


@pytest.mark.django_db
def test_create_board_category(auth_client, board):
    url = reverse('category_create')
    expected_response = {
        'title': 'unq',
        'board': board.pk
    }
    response = auth_client.post(
        path=url,
        data=expected_response
    )

    response_data = response.json()

    assert response_data.get('board') == board.id


@pytest.mark.django_db
def test_category_404_httpstatus(auth_client, category, user_fixture):
    url = reverse('category', kwargs={'pk': category.pk})

    response = auth_client.get(path=url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
