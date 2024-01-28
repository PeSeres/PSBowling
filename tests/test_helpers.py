import pytest

from src.helpers import is_valid_input, is_strike, is_spare


@pytest.mark.parametrize("value, expected", [
    ('', True), ('X', True), ('x', True), ('/', True),
    ('0', True), ('1', True), ('2', True), ('3', True),
    ('4', True), ('5', True), ('6', True), ('7', True),
    ('8', True), ('9', True), ('a', False), ('10', False), ('-1', False)
])
def test_is_valid_input(value, expected):
    assert is_valid_input(value) == expected


@pytest.mark.parametrize("value, expected", [
    ('X', True), ('x', True), ('', False), ('/', False),
    ('0', False), ('1', False), ('2', False), ('3', False),
    ('4', False), ('5', False), ('6', False), ('7', False),
    ('8', False), ('9', False), ('a', False)
])
def test_is_strike(value, expected):
    assert is_strike(value) == expected


@pytest.mark.parametrize("value, expected", [
    ('/', True), ('X', False), ('x', False), ('', False),
    ('0', False), ('1', False), ('2', False), ('3', False),
    ('4', False), ('5', False), ('6', False), ('7', False),
    ('8', False), ('9', False), ('a', False)
])
def test_is_spare(value, expected):
    assert is_spare(value) == expected
