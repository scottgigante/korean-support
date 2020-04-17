import pytest
from unittest.mock import patch
from korean.edit_functions import add_diaeresis
from korean.edit_functions import english
from korean.edit_functions import translate_local
from .fixtures.fixtures_edit_functions import mocked_krneng_dic


# db tests modeled off results from: https://github.com/garfieldnate/kengdic
@pytest.mark.parametrize(
    "test_search_hangul, expected_english_res",
    [("밥", ["rice, a meal"]), ("사랑", ["love"]), ("나라", ["country"])],
)
def test_translate_local_single_result(
    test_search_hangul, expected_english_res, mocked_krneng_dic
):
    mocked_krneng_dic.search.return_value = expected_english_res
    assert translate_local(test_search_hangul) == expected_english_res


@pytest.mark.parametrize(
    "test_search_hangul, expected_english_res",
    [
        ("밥", ["rice", "a rice bowl"]),
        ("사랑", ["love", "endearing"]),
        ("나라", ["country", "islander"]),
    ],
)
def test_translate_local_multiple_results(
    test_search_hangul, expected_english_res, mocked_krneng_dic
):
    mocked_krneng_dic.search.return_value = expected_english_res
    assert translate_local(test_search_hangul) == expected_english_res


# TODO: translate_local failure case.


@pytest.mark.parametrize(
    "test_str, expected_str", [("v", "ü"), ("very", "üery"), ("vlo", "ülo")]
)
def test_add_diaeresis(test_str, expected_str):
    assert add_diaeresis(test_str) == expected_str
