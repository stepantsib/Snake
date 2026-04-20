import pytest
from src.element import Element


def test_element_creation():
    e = Element(5, 10)
    assert e.x == 5
    assert e.y == 10


def test_element_equality():
    e1 = Element(3, 7)
    e2 = Element(3, 7)
    e3 = Element(4, 7)
    assert e1 == e2
    assert e1 != e3
    assert hash(e1) != hash(e3)