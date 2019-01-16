import pytest

from dewar.parser import parse_path, fill_path


@pytest.mark.parametrize("path,out", [
    ("/novar/", []),
    ("/<one_var>/", ["one_var"]),
    ("/<many>/<var>/", ["many", "var"])
])
def test_parse(path, out):
    assert(parse_path(path) == out)


@pytest.mark.parametrize("path,elems,out", [
    ("/novar/", [],  "/novar/"),
    ("/<one_var>/", "var", "/var/"),
    ("/<one_var>/", tuple(["var"]), "/var/"),
    ("/<many>/<var>/", ("one", "two"), "/one/two/")
])
def test_parse(path, elems, out):
    assert(fill_path(path, elems) == out)
