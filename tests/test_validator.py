import pytest

from dewar.validator import validate_page
from dewar.exceptions import ValidationError


def func_with_path(path, returns):
    def anon():
        return returns
    anon.name = "name"
    anon.path = path
    return anon


@pytest.mark.parametrize(
    "func,error",
    [
        (func_with_path("/<test>/", "string"), "requires variables"),
        (func_with_path("/static_page.html", {"string": "fail"}), "did not specify variables"),
        (func_with_path("/static_page.html", None), "not return a valid object"),
    ]
)
def test_validate_page_errors(func, error):
    with pytest.raises(ValidationError, match=error):
        validate_page(func)


@pytest.mark.parametrize(
    "func",
    [
        (func_with_path('/index.html', "test")),
        (func_with_path('/<test>/index.html', {('test'): "test"})),
        (func_with_path('/<test>/<test2>.html', {('test', 'test'): "test"})),
    ]
)
def test_validation_passes(func):
    assert validate_page(func)
