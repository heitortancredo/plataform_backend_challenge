import sys
import os
import pytest
import time

sys.path.append("../src")
from app import create_app

def send_product(client, _id, name):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    payload = {
        'id': _id,
        'name': name
    }
    rv = client.post('/v1/products', json=payload, headers=headers, follow_redirects=True)

    return rv.status


@pytest.fixture
def app():
    app = create_app(config='test.cfg')
    return app


def test_dup_product(client):

    expected_OK = "200 OK"
    reason = send_product(client, 'Teste', 123)
    assert expected_OK == reason

    expected_NOK = "403 FORBIDDEN"
    reason = send_product(client, 'Teste', 123)
    assert expected_NOK == reason

def test_rate_limit_OK(client):
    reason = send_product(client, 'Teste 3', 124)
    time.sleep(3)
    reason = send_product(client, 'Teste 3', 124)

    expected_OK = "200 OK"

    assert expected_OK == reason

def test_rate_limit_NOK(client):
    reason = send_product(client, 'Teste 4', 125)
    reason = send_product(client, 'Teste 4', 125)

    expected_NOK = "403 FORBIDDEN"

    assert expected_NOK == reason

def test_distinct_products(client):

    expected_OK = "200 OK"

    reason = send_product(client, 'Teste 5', 126)
    assert expected_OK == reason

    reason = send_product(client, 'Teste 6', 127)
    assert expected_OK == reason
