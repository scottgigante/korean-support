import pytest


@pytest.fixture()
def mocked_krneng_dic(mocker):
    return mocker.patch("korean.edit_functions.db")
