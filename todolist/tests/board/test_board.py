import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_board_create(auth_client):
    url = reverse('board_create')
    expected_response = {
        'title': 'test_name'
    }
    response = auth_client.post(
        path=url,
        data=expected_response
    )
    response_data = response.json()

    assert response_data.get('title') == expected_response.get('title')


@pytest.mark.django_db
def test_board_status_create(auth_client):
    url = reverse('board_create')
    expected_response = {
        'title': 'test_name'
    }
    response = auth_client.post(
        path=url,
        data=expected_response
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_board_url_create(auth_client):
    url = reverse('board_create')

    assert url == '/goals/board/create'


@pytest.mark.django_db
def test_board_is_delete_create(auth_client):
    url = reverse('board_create')

    expected_response = {
        'title': 'test_name',
    }
    response = auth_client.post(
        path=url,
        data=expected_response
    )
    response_data = response.json()

    assert response_data.get('is_deleted') is False


@pytest.mark.django_db
def test_board_no_work_create(auth_client):
    url = reverse('board_create')

    expected_response = {
        'title': False,
    }
    auth_client.post(
        path=url,
        data=expected_response
    )

    assert AssertionError


@pytest.mark.django_db
def test_board_404_httpstatus(auth_client, board):
    url = reverse('board', kwargs={'pk': board.pk})
    response = auth_client.get(path=url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
