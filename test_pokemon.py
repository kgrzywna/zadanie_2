import pytest
from pokemon import *


def test_result():
    data = [{"fire": ["grass"]}]

    assert make_requests(data) == ["2x"]


def test_parse():
    data = ['fire -> dark normal', 'rock -> grass']

    expected_result = [
        {"fire": ["dark", "normal"]},
        {"rock": ["grass"]}
    ]

    assert parse_data(data) == expected_result


def test_http_exception():
    data = [{'asdf': ['grass']}]

    with pytest.raises(Exception):
        make_requests(data)


def test_value_exception():
    data = [""]

    with pytest.raises(ValueError):
        make_requests(data)
