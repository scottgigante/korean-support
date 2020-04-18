import pytest


class MockWordObject:
    """Mock word object for testing."""

    def __init__(self):
        self.english = ""


@pytest.fixture()
def mocked_krneng_dic(mocker):
    return mocker.patch("korean.edit_functions.db")


@pytest.fixture()
def mocked_translate_local(mocker):
    return mocker.patch("korean.edit_functions.translate_local")
