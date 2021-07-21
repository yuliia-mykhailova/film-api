"""Module for genre testing"""

import requests


def test_genre():
    """Test get genres"""
    url = "http://0.0.0.0:5000/genres"

    response = requests.get(url)
    assert response.status_code == 200


def test_post_genres():
    """Test post genres"""
    response = requests.post('http://0.0.0.0:5000/genres',
                             json={"genre_title": "Drama"})
    assert response.status_code == 401


def test_delete_genres():
    """Test delete genres"""
    response = requests.delete('http://0.0.0.0:5000/genres/1')
    assert response.status_code == 401
