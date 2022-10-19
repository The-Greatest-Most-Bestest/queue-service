import pytest
import requests

from bs4 import BeautifulSoup as BS

@pytest.fixture()
def request_url():
    return 'https://github.com/RKuttruff/incubator-sdap-nexus/blob/CDMS-122/data-access/tests/test_zarr.py'
            # URL points to a suite of unit tests I wrote for my internship


# We haven't got any backend code to run unit tests against so I will just quickly demo that I know how to write test cases with pytest

def test_passing():
    assert 4 == (2+2)
    assert 1 > -43

def test_failing():
    assert len("this will fail") == 15

def test_error():
    open('this_file_does_not_exist.yml')

def test_request_and_fixture(request_url):
    response = requests.get(request_url)

    assert response.status_code == 200

    soup = BS(response.text, 'html.parser')

@pytest.mark.skip
def test_skip():
    pass

@pytest.mark.xfail
def test_expected_failure():
    assert False