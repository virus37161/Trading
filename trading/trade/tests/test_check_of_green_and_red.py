from django.test import TestCase
from unittest.mock import patch
import pytest
from ..services.signal_1 import check_of_green_and_red

list_short = [
    ['3123123', '10', '432', '432', '4', '432', '432'],
    ['23412412', '5', '432', '432', '6', '432', '432'],
    ['3123123', '10', '432', '432', '4', '432', '432'],
]
list_long = [
    ['3123123', '5', '432', '432', '6', '432', '432'],
    ['23412412', '10', '432', '432', '4', '432', '432'],
    ['3123123', '5', '432', '432', '6', '432', '432'],

]

@pytest.mark.parametrize("data", [(list_long),(list_short)])
def test_check_of_green_and_red(data):
    assert check_of_green_and_red(data) == True


