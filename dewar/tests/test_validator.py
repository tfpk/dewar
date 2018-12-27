import pytest

from dewar.validator import validate_dict, validate_page
from dewar.exceptions import ValidationError

@pytest.mark.parametrize(
    "input_dict,tags,error",
    [
        ({1: "fail"}, [1], "did not contain keys"),
        ({1: "fail", 2: "also_fail"}, [1, 2], "did not contain keys"),
        ({"string": "fail"}, [1, 2], "strings as keys"),
        ({(1, 2): "fail"}, [1], "incorrect number of variables"),
        ({tuple([1]): "fail", (1, 2): "pass"}, [1, 2], "incorrect number of variables"),
    ]
)
def test_validate_dict_errors(input_dict, tags, error):
    with pytest.raises(ValidationError, match=error):
        validate_dict(input_dict, tags, "name")



@pytest.mark.parametrize(
    "input_dict,tags",
    [
        ({}, [1]),
        ({}, [1, 2]),
        ({"name": "pass"}, [1]),
        ({tuple(["name"]): "pass"}, [1]),
        ({("name", "name2"): "pass"}, [1, 2]),
        ({("name", "name2"): "pass", ("1", "2"): "test"}, [1, 2]),
    ]
)
def test_validate_dict_passes(input_dict, tags):
    assert validate_dict(input_dict, tags, "name")

def func_with_path(path):
    def anon():
        pass
    anon.name = "name"
    anon.path = path
    return anon

@pytest.mark.parametrize(
    "input_dict,func,error",
    [
        ("string", func_with_path("/<test>/"), "requires variables"),
        ({"string": "fail"}, func_with_path("/static_page.html"), "did not specify variables"),
        (None, func_with_path("/static_page.html"), "not return a valid object"),
    ]
)
def test_validate_page_errors(input_dict, func, error):
    with pytest.raises(ValidationError, match=error):
        validate_page(input_dict, func)


@pytest.mark.parametrize(
    "input_dict,func",
    [
        ("test", func_with_path('/index.html')),
        ({('test'): "test"}, func_with_path('/<test>/index.html')),
        ({('test', 'test'): "test"}, func_with_path('/<test>/<test2>.html')),
    ]
)
def test_validation_passes(input_dict, func):
    assert validate_page(input_dict, func)

