"""Módulo para evaluar funciones matemáticas"""
import pytest
from src import math_func


# tipificar la salida: número, string
@pytest.mark.number
def test_add():
    """
    Evaluar la función 'add'
    """
    assert math_func.add(7, 3) == 10
    assert math_func.add(7) == 9


@pytest.mark.number
def test_product():
    """
    Evaluar la función producto
    """
    assert math_func.product(5, 5) == 25
    assert math_func.product(5) == 10


@pytest.mark.strings
def test_add_strings():
    """
    Evaluar la función 'add'
    """
    result = math_func.add('Hello', ' World')
    assert result == 'Hello World'
    assert isinstance(result, str)
    assert 'Hello' in result


@pytest.mark.strings
def test_product_strings():
    """
    Evaluar la función producto
    """
    assert math_func.product('Hello ', 3) == 'Hello Hello Hello '
    result = math_func.product('Hello ')
    assert result == 'Hello Hello '
    assert isinstance(result, str)
    assert 'Hello' in result
