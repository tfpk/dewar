import os
import pytest
import time

from pathlib import Path

from dewar.exceptions import ValidationError

from fixtures.site import site, full_site

@pytest.mark.parametrize("page_name", [
    ("index.html"),
    ("inside_dir/index.html")
])
def test_single_render(tmp_path, site, page_name):
    PAGE_TEXT = "test"

    @site.register(page_name)
    def index():
        return PAGE_TEXT

    site.render(path=tmp_path)

    with open(tmp_path / page_name, 'r') as page:
        assert(page.read() == PAGE_TEXT)


def test_one_var_render(tmp_path, site):
    PAGE_TEXT = {
        "test": "TEST"
    }

    @site.register("<one_var>/index.html")
    def one_index():
        return PAGE_TEXT

    site.render(path=tmp_path)

    with open(tmp_path / "test/index.html", 'r') as page:
        assert(page.read() == "TEST")


def test_multi_var_render(tmp_path, site):
    PAGE_TEXT = {
        ("dir", "index"): "inside index",
        ("dir", "help"): "inside help",
        ("dir_two", "other"): "inside other"
    }

    @site.register("<one_var>/<two_var>.html")
    def one_index():
        return PAGE_TEXT

    site.render(path=tmp_path)

    for key in PAGE_TEXT:
        with open(tmp_path / f"{key[0]}/{key[1]}.html", 'r') as page:
            assert(page.read() == PAGE_TEXT[key])


@pytest.mark.parametrize("page_name", [
    ("/index.html"),
    ("/inside_dir/index.html"),
    ("/<one_var>/index.html"),
    ("/<one_var>/<two_var>.html"),
])
def test_starts_slash_error(tmp_path, site, page_name):

    with pytest.raises(ValueError, match="can't begin with"):
        @site.register(page_name, validate=False)
        def index():
            return None


def test_render_chain(tmp_path, site):
    PAGE_TEXT = {
        "index": "inside index",
        "help": "inside help",
        "other": "inside other"
    }

    @site.register("list.html")
    def list():
        x = sorted(multi_index().keys())
        return ', '.join(x)

    @site.register("pages/<two_var>.html")
    def multi_index():
        return PAGE_TEXT

    site.render(path=tmp_path)

    for key in PAGE_TEXT:
        with open(tmp_path / f"pages/{key}.html", 'r') as page:
            assert(page.read() == PAGE_TEXT[key])

    with open(tmp_path / "list.html", "r") as page:
        assert(page.read() == "help, index, other")


def test_single_page_consistency(site):

    @site.register('random_page.html')
    def random_page():
        return f"function called at: {time.time()}"

    first_call = random_page()
    time.sleep(0.01)
    second_call = random_page()
    assert(first_call == second_call)


def test_multi_page_consistency(site):

    @site.register('<i>/index.html')
    def random_multi_page():
        return {
            "1": f"1function called at: {time.time()}",
            "2": f"2function called at: {time.time()}",
        }

    first_call = random_multi_page()
    time.sleep(0.01)
    second_call = random_multi_page()
    assert(first_call == second_call)


def test_page(site):
    PAGE_PATH = "random_page.html"

    @site.register(PAGE_PATH)
    def random_page():
        path = random_page.path
        name = random_page.__name__
        return f"path: {path}, name: {name}"

    assert(random_page.path == PAGE_PATH)
    assert(random_page.name == "random_page")

    assert(random_page() == f"path: {PAGE_PATH}, name: random_page")

    assert(random_page.path == PAGE_PATH)
    assert(random_page.name == "random_page")


def test_validation(site):
    with pytest.raises(ValidationError, match="did not return"):
        @site.register('fail_path')
        def fail_path():
            return None
        fail_path()

    @site.register('fail_path_novalidate', validate=False)
    def fail_path_novalidate():
        return None
    fail_path_novalidate()

    @site.register('str_path')
    def str_path():
        return "string path successfuly prints"
    str_path()

    @site.register('dict_path/<term>')
    def dict_path():
        return {
            ('1',): "text for 1",
            ('2',): "text for 2",
        }


@pytest.mark.parametrize('call_self', [True, False])
def test_recursion_error(site, call_self):
    @site.register('a')
    def a():
        if call_self:
            a()
        else:
            b()

    @site.register('b')
    def b():
        a()

    with pytest.raises(RuntimeError, match="within themselves"):
        a()


def test_static_move(tmp_path, full_site):
    full_site.render(path=tmp_path)
    assert(Path(tmp_path / 'static' / 'static_file').is_file())
