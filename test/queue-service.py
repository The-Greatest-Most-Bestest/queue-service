import pytest
import requests

from queueservice.request_handler import Handler

from bs4 import BeautifulSoup as BS


state = [
    {
        "id": '0',
        "queue": ['0', '1', '2']
    }
]

@pytest.fixture()
def request_url():
    return 'https://github.com/RKuttruff/incubator-sdap-nexus/blob/CDMS-122/data-access/tests/test_zarr.py'


def mock_query(s):
    global state

    item = state[0]

    return item['queue']

def mock_update(id, l):
    global state

    state[0]['queue'] = l

@pytest.fixture(scope='module')
def mock():
    handler = Handler()

    handler.proxy.query = mock_query
    handler.proxy.update = mock_update

    return handler

# We haven't got any backend code to run unit tests against so I will just quickly demo that I know how to write test cases with pytest

def test_enqueue(mock):
    response = mock.enqueue('4', '0')

    assert response['success']
    assert response['position'] == 4

