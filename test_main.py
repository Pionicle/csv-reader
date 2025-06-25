import pytest

from table_operations import (
    convert_type,
    get_table,
    where_table,
    aggregate_table,
    order_by_table,
)

test_file_csv = "test_fruits.csv"


@pytest.mark.parametrize(
    "value, expected",
    [
        ("5", 5),
        ("5.0", 5.0),
        ("123", 123),
        ("123.456", 123.456),
        ("True", True),
        ("False", False),
        ("None", None),
    ],
)
def test_convert_type(value, expected):
    assert convert_type(value) == expected


def test_get_table():
    table = get_table(test_file_csv)
    assert len(table) == 4
    assert table == [
        {"name": "apple", "price": 5.0, "is_sweet": True},
        {"name": "banana", "price": 12.5, "is_sweet": True},
        {"name": "orange", "price": 7.8, "is_sweet": False},
        {"name": "pear", "price": 1, "is_sweet": None},
    ]


@pytest.mark.parametrize(
    "where, expected",
    [
        ("name=apple", [{"name": "apple", "price": 5.0, "is_sweet": True}]),
        ("price>10", [{"name": "banana", "price": 12.5, "is_sweet": True}]),
        (
            "price<5.5",
            [
                {"name": "apple", "price": 5.0, "is_sweet": True},
                {"name": "pear", "price": 1, "is_sweet": None},
            ],
        ),
        ("price=12.5", [{"name": "banana", "price": 12.5, "is_sweet": True}]),
        ("is_sweet=False", [{"name": "orange", "price": 7.8, "is_sweet": False}]),
    ],
)
def test_where_table(where, expected):
    table = get_table(test_file_csv)
    assert where_table(table, where) == expected


@pytest.mark.parametrize(
    "aggregate, expected",
    [
        ("price=avg", [{"avg": 6.575}]),
        ("price=min", [{"min": 1}]),
        ("price=max", [{"max": 12.5}]),
    ],
)
def test_aggregate_table(aggregate, expected):
    table = get_table(test_file_csv)
    assert aggregate_table(table, aggregate) == expected


@pytest.mark.parametrize(
    "order_by, expected",
    [
        (
            "price=asc",
            [
                {"name": "pear", "price": 1, "is_sweet": None},
                {"name": "apple", "price": 5.0, "is_sweet": True},
                {"name": "orange", "price": 7.8, "is_sweet": False},
                {"name": "banana", "price": 12.5, "is_sweet": True},
            ],
        ),
        (
            "price=desc",
            [
                {"name": "banana", "price": 12.5, "is_sweet": True},
                {"name": "orange", "price": 7.8, "is_sweet": False},
                {"name": "apple", "price": 5.0, "is_sweet": True},
                {"name": "pear", "price": 1, "is_sweet": None},
            ],
        ),
    ],
)
def test_order_by_table(order_by, expected):
    table = get_table(test_file_csv)
    assert order_by_table(table, order_by) == expected
