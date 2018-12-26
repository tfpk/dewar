import os
import pytest
import time

from fixtures.site import site

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


def test_page_consistency(site):
   
    @site.register('random_page.html')
    def random_page():
        return f"function called at: {time.time()}"

    first_call = random_page()
    time.sleep(0.01)
    second_call = random_page()
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

