import pytest
from unittest.mock import patch
from korean.edit_functions import add_diaeresis
from korean.edit_functions import english
from korean.edit_functions import translate_local
from korean.edit_functions import no_hidden
from korean.edit_functions import no_color
from korean.edit_functions import silhouette
from korean.edit_functions import hanja
from .fixtures.fixtures_edit_functions import mocked_krneng_dic
from .fixtures.fixtures_edit_functions import mocked_translate_local
from .fixtures.fixtures_edit_functions import MockWordObject


@pytest.mark.parametrize(
    "test_txt, expected_txt",
    [
        (None, ""),
        ("<!--txt--><p>txt</p>", "<p>txt</p>"),
        ("&nbsp;", ""),
        ("<font color=></font>", ""),
        ("<span style=></span>", ""),
    ],
)
def test_no_color(test_txt, expected_txt):
    assert no_color(test_txt) == expected_txt


@pytest.mark.parametrize(
    "test_hangul, expected_hangul", [("한글", "_ _"), ("한국C", "_ _C")]
)
def test_silhouette(test_hangul, expected_hangul):
    assert silhouette(test_hangul) == expected_hangul


@pytest.mark.parametrize(
    "test_txt, expected_txt",
    [
        ("<!--txt-->", ""),
        ("<p>txt</p>", "<p>txt</p>"),
        ("<!--txt--><p>txt</p>", "<p>txt</p>"),
    ],
)
def test_no_hidden(test_txt, expected_txt):
    assert no_hidden(test_txt) == expected_txt


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


def test_english(mocked_translate_local):
    mwo_밥_first = MockWordObject()
    mwo_밥_second = MockWordObject()

    mwo_밥_first.english = "a meal"
    mwo_밥_second.english = "rice"

    mock_translate_local_results = [mwo_밥_first, mwo_밥_second]

    mocked_translate_local.return_value = mock_translate_local_results

    expected_built_str = "a meal\n<br>rice"

    assert english("밥") == expected_built_str


def test_hanja(mocked_translate_local):
    # these hanja are unrelated, but used for unittesting purposes

    mwo_밥_first = MockWordObject()
    mwo_일월_second = MockWordObject()

    mwo_밥_first.english = "食"
    mwo_일월_second.english = "一月"

    mock_translate_local_results = [mwo_밥_first, mwo_일월_second]

    mocked_translate_local.return_value = mock_translate_local_results

    expected_built_str = "食,一月"


@pytest.mark.parametrize(
    "test_str, expected_str", [("v", "ü"), ("very", "üery"), ("vlo", "ülo")]
)
def test_add_diaeresis(test_str, expected_str):
    assert add_diaeresis(test_str) == expected_str
