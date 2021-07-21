"""Test model User"""

import requests


def test_user_add():
    """Add new user"""
    url = "http://0.0.0.0:5000/users"

    response = requests.post(url,
                             json={
                                 "first_name": "Yuliia",
                                 "last_name": "Mykhailova",
                                 "email": "yuliia@gmail.com",
                                 "password": "123456",
                                 "is_admin": 1})
    assert response.status_code == 201


def test_user_validation_password():
    """Wrong password format"""
    url = "http://0.0.0.0:5000/users"

    response = requests.post(url,
                             json={
                                 "first_name": "Yuliia",
                                 "last_name": "Mykhailova",
                                 "email": "yuliia123@gmail.com",
                                 "password": "123"
                             })
    assert response.status_code == 500


def test_user_login():
    """Test login"""
    url = "http://0.0.0.0:5000/login"
    res = requests.post(url,
                        json={
                            "email": "yuliia@gmail.com",
                            "password": "123456"
                        })
    assert res.status_code == 200


def test_get_users():
    """Test get users"""
    res = requests.get('http://0.0.0.0:5000/users')
    assert res.status_code == 401


def test_get_user_by_id():
    """Test get user by id"""
    res = requests.get('http://0.0.0.0:5000/users/1')
    assert res.status_code == 401


def test_delete_user():
    """Test delete user"""
    res = requests.delete("http://0.0.0.0:5000/users/1")
    assert res.status_code == 401
