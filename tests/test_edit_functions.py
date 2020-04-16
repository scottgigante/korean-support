import pytest
from korean.edit_functions import add_diaeresis


@pytest.mark.parametrize(
    "test_str, expected_str", [("v", "ü"), ("very", "üery"), ("vlo", "ülo")]
)
def test_add_diaeresis(test_str, expected_str):
    assert add_diaeresis(test_str) == expected_str
