from datetime import date
from typing import List, Dict
from unittest.mock import patch
from app.main import outdated_products


def test_outdated_products() -> None:
    products: List[Dict[str, object]] = [
        {
            "name": "salmon",
            "expiration_date": date(2022, 2, 10),
            "price": 600
        },
        {
            "name": "chicken",
            "expiration_date": date(2022, 2, 5),
            "price": 120
        },
        {
            "name": "duck",
            "expiration_date": date(2022, 2, 1),
            "price": 160
        }
    ]

    # Маскируем datetime.date.today() для тестирования
    with patch("datetime.date") as mock_date:
        # мокаем текущую дату н 2 февраля 2022 года
        mock_date.today.return_value = date(2022, 2, 2)

        # Проверяем результат
        assert outdated_products(products) == ["duck"]


def test_outdated_products_no_expired() -> None:
    products: List[Dict[str, object]] = [
        {
            "name": "salmon",
            "expiration_date": date(2022, 2, 10),
            "price": 600
        },
        {
            "name": "chicken",
            "expiration_date": date(2022, 2, 5),
            "price": 120
        }
    ]

    with patch("datetime.date") as mock_date:
        # мокаем текущую дату на 1 февраля 2022 года
        mock_date.today.return_value = date(2022, 2, 1)

        # Проверяем результат
        assert outdated_products(products) == []


def test_outdated_products_all_expired() -> None:
    products: List[Dict[str, object]] = [
        {
            "name": "salmon",
            "expiration_date": date(2022, 2, 1),
            "price": 600
        },
        {
            "name": "chicken",
            "expiration_date": date(2022, 1, 31),
            "price": 120
        }
    ]

    with patch("datetime.date") as mock_date:
        # Устанавливаем текущую дату на 2 февраля 2022 года
        mock_date.today.return_value = date(2022, 2, 2)

        # Проверяем результат
        assert outdated_products(products) == ["salmon", "chicken"]


def test_expiration_day_today_not_outdated() -> None:
    products: List[Dict[str, object]] = [
        {
            "name": "salmon",
            "expiration_date": date(2022, 2, 2),  # Срок годности истекает сегодня
            "price": 600
        }
    ]

    with patch("datetime.date") as mock_date:
        # Устанавливаем текущую дату на 2 февраля 2022 года
        mock_date.today.return_value = date(2022, 2, 2)

        # Проверяем результат
        assert outdated_products(products) == []
