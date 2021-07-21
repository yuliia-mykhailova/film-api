"""Module for director testing"""

import requests


def test_get_directors():
    """Test get directors"""
    response = requests.get('http://0.0.0.0:5000/directors')
    assert response.status_code == 200


def test_get_id_director():
    """Test get director by id"""
    response = requests.get('http://0.0.0.0:5000/directors/1')
    assert response.status_code == 404


def test_post_directors():
    """Test post directors"""
    response = requests.post('http://0.0.0.0:5000/directors',
                             json={
                                 "first_name": "Christopher",
                                 "last_name": "Nolan"
                             })
    assert response.status_code == 401


def test_delete_directors():
    """Test delete directors"""
    response = requests.delete('http://0.0.0.0:5000/directors/3')
    assert response.status_code == 401
