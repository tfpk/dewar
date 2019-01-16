from dewar._internal import get_caller_location, get_closest_path, get_closest_site
from dewar import Site

from fixtures.site import site

from pathlib import Path

import pytest


def test_caller_loc():
    def make_call():
        return get_caller_location()
    assert(make_call() == Path(__file__).parent)
    assert(get_caller_location() != Path(__file__).parent)
    # calling function with this means stack contains filename as eval
    with pytest.raises(RuntimeError, match="caller location"):
        eval('(lambda x: get_caller_location())(1)')


def test_closest_path(site):
    PATH = "page/index"

    def assert_correct_path():
        path = get_closest_path()
        assert(path == PATH)

    @site.register(PATH)
    def get_path():
        assert_correct_path()
        assert(get_closest_path() == PATH)


def test_closest_site(site):
    PATH = "page/site"

    def assert_correct_site():
        assert(site == get_closest_site())

    @site.register(PATH)
    def get_path():
        assert_correct_site()
        assert(site == get_closest_site())


def test_closest_site_multi():
    site_a = Site()
    site_b = Site()
    # TODO: START HERE

    @site_a.register('tests')
    def test():
        assert(site == site_a)
