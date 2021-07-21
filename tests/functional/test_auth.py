"""Module for testing login, signup, logout"""
import requests
from flask import json
import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_create():
    url = "http://0.0.0.0:5000/users"

    response = requests.post(url,
                             json={
                                 "first_name": "test",
                                 "last_name": "test",
                                 "email": "test@gmail.com",
                                 "password": "123456",
                                 "is_admin": 1})
    assert response.status_code == 201


def test_login():
    url = "http://0.0.0.0:5000/login"

    response = requests.post(url,
                             json={
                                 "email": "test@gmail.com",
                                 "password": "123456"
                             })
    assert response.status_code == 200


def test_logout(client):
    url = "http://0.0.0.0:5000/logout"
    response = client.post(url)
    assert response.status_code == 200
