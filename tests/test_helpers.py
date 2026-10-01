import pytest

from notebooks.helpers import layer_path, parse_keys, spark_type_for, to_snake_case


@pytest.mark.parametrize("raw,expected", [
    ("ORDER_ID", "order_id"),
    ("LastUpdateDt", "last_update_dt"),
    ("  Gross Amount ($) ", "gross_amount"),
])
def test_snake_case(raw, expected):
    assert to_snake_case(raw) == expected


def test_parse_keys():
    assert parse_keys("ENTRY_ID, LINE_NO") == ["entry_id", "line_no"]


def test_layer_path():
    assert layer_path("silver", "ORACLE", "ORDERS").endswith("/oracle/orders")
    with pytest.raises(ValueError):
        layer_path("platinum", "x", "y")


def test_type_map():
    assert spark_type_for("NUMBER(10,2)") == "decimal(38,10)"
    assert spark_type_for("XMLTYPE") == "string"
