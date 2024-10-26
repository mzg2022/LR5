import pytest
import time
from currencies import Currencies


def test_get_currencies():
    """Тест на корректное получение курсов валют."""
    cur = Currencies()
    result = cur.get_currencies(['R01035', 'R01239', 'R01720'])
    assert len(result) == 3, "Ожидалось три валюты в списке"


def test_invalid_currency_id():
    """Тест на случай, если указан неверный ID валюты."""
    cur = Currencies()

    time.sleep(1)

    result = cur.get_currencies(['R9999'])
    assert result == [{'R9999': None}], "Неверный ID должен вернуть словарь с None"


def test_request_interval():
    """Тест на проверку частоты запросов."""
    cur = Currencies(request_interval = 1)  # интервал 1 секунда
    time.sleep(1)
    cur.get_currencies(['R01035'])  # первый запрос
    time.sleep(1)  # пауза, чтобы запрос прошел снова
    cur.get_currencies(['R01035'])  # второй запрос, должен пройти успешно


def test_visualize_currencies():
    """Тест для метода визуализации курсов валют."""
    cur = Currencies()
    time.sleep(1)
    result = cur.get_currencies(['R01035', 'R01335'])
    cur.visualize_currencies(result, show_plot=False, save_fig=False)
    assert True, "Визуализация прошла успешно"
