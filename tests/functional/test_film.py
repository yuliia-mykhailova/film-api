"""Module for film testing"""

import requests


def test_film_get():
    """Test get films"""
    url = "http://0.0.0.0:5000/films"
    response = requests.get(url)
    assert response.status_code == 200


def test_err_get_film_id():
    """Test get film by id"""
    url = "http://0.0.0.0:5000/films/15"
    response = requests.get(url)
    assert response.status_code == 404


def test_film_search():
    """Test get films with search by name"""
    url = "http://0.0.0.0:5000/films?search=bat"
    response = requests.get(url)
    assert response.status_code == 200


def test_film_filter_genre():
    """Test get films by genre"""
    url = "http://0.0.0.0:5000/films?genre=horror"
    response = requests.get(url)
    assert response.status_code == 404


def test_film_filter_years_release():
    """Test get films between release years"""
    url = "http://0.0.0.0:5000/films?year_from=1999&year_to=2020"
    response = requests.get(url)
    assert response.status_code == 200


def test_film_filter_director():
    """Test get films by director"""
    url = "http://0.0.0.0:5000/films?director=Christopher%20Nolan"
    response = requests.get(url)
    assert response.status_code == 404


def test_post_film():
    """Test post film"""
    response = requests.post('http://0.0.0.0:5000/films', json={
        "film_title": "Batman",
        "release_date": "2021-07-21T20:45:04.327328422Z",
        "description": "smth",
        "rating": 7,
        "poster": "www",
        "director_first_name": "Christopher",
        "director_last_name": "Nolan",
        "genres": ["Drama"]
    })
    assert response.status_code == 401


def test_delete_films_by_id():
    """Test delete film"""
    response = requests.delete('http://0.0.0.0:5000/films/1')
    assert response.status_code == 401
