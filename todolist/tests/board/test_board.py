import pytest
from django.urls import reverse
from rest_framework import status

from goals.serializers import BoardListSerializer
from tests.factories import BoardFactory, UserFactory


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
def test_board_create(auth_client):
    url = reverse('board_create')
    expected_response = {
        'title': 'test_name'
    }
    response = auth_client.post(
        path=url,
        data=expected_response
    )

    assert response.status_code == status.HTTP_201_CREATED


#
# @pytest.mark.django_db
# def test_board_list(auth_client):
#     url = reverse('board_list')  # берётся из атрибута "name" urls.path
#     boards = BoardFactory.create_batch(3)  # кол-во записей в списке для тестирования
#     expected_response = {
#         'count': 3,
#         'next': None,
#         'previous': None,
#         'results': BoardListSerializer(instance=boards, many=True).data
#     }
#
#     response = auth_client.get(
#         path=url,
#         data=expected_response)
#
#     response_data = response.json()
#
#     assert response.status_code == 403, 'boards статус не 200'
#     assert response_data == expected_response, 'boards data не совпала'
#
#
@pytest.mark.django_db
def test_board(auth_client, board):
    url = reverse('board', kwargs={'pk': board.pk})
    response = auth_client.get(path=url)
    assert response.status_code == status.HTTP_200_OK
