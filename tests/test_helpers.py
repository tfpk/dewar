import pytest
import time
import dewar

from dewar.helpers import *
from dewar.dewar import Site

from fixtures.site import site, full_site


def test_site_property(tmp_path):
    def func():
        # TODO: follow me down to figure out why it recurrs.
        assert(hasattr(dewar.site, 'register'))
        return "rendered"

    site_instance = dewar.Site()
    func = site_instance.register('test.html')(func)
    site_instance.render(path=tmp_path)


def test_site_property_error(): 
    with pytest.raises(RuntimeError, match="could not be found"):
        # assert necessary becasue proxy only errs on attr access
        assert(hasattr(dewar.site, 'deregister'))


def test_multiple_site_error():
    a = Site()
    b = Site()
    assert(dewar.site == b)
    assert(dewar.site != a)


def test_freeze_func_no_parens():
    @freeze_func
    def test():
        return f"function called at: {time.time()}"

    first_call = test()
    time.sleep(0.001)
    second_call = test()
    assert(first_call == second_call)


def test_freeze_func_w_parens():
    @freeze_func()
    def test():
        return f"function called at: {time.time()}"

    first_call = test()
    time.sleep(0.001)
    second_call = test()
    assert(first_call == second_call)


@pytest.mark.parametrize('arg1,kwarg1,arg2,kwarg2', [
    (('arg1',), {}, ('arg2',), {}),
    (('arg1',), {'kw': 1}, ('arg2',), {'kw': 1}),
    (('arg',), {'kw': 1}, ('arg',), {'kw': 2}),
    (('arg1',), {'kw': 1}, ('arg2',), {'kw': 2}),
    (tuple(), {'kw': 1}, tuple(), {'kw': 2})
])
def test_freeze_func_args(arg1, kwarg1, arg2, kwarg2):
    @freeze_func()
    def test(*args, **kwargs):
        return f"function called at: {time.time()}"

    first_call = test(*arg1, **kwarg1)
    time.sleep(0.001)
    same_call = test(*arg1, **kwarg1)
    diff_call = test(*arg2, **kwarg2)
    assert(first_call == same_call)
    assert(first_call != diff_call)


def test_load_data(full_site):
    assert(load_data('test_data') == 'test\n')


def test_load_data_dir(full_site):
    assert load_data_dir('data_dir') == {
        'data_1': 'data_1\n',
        'data_2': 'data_2\n',
    }
    assert load_data_dir('data_dir/dir') == {
        'data_3': 'data_3\n'
    }


def test_load_json():
    assert(load_json('{"a": ["b", "c"]}') == {'a': ['b', 'c']})


def test_load_json_data(full_site):
    assert(load_json_data('test_json') == {'a': ['b', 'c']})


def test_load_md():
    TEST_STRING = "# Title\n_italic_ **bold**"
    TEST_STRING_RESULT = "<h1>Title</h1>\n<p><em>italic</em> <strong>bold</strong></p>"

    assert(load_md(TEST_STRING) == TEST_STRING_RESULT)


def test_load_md_data(full_site):
    TEST_STRING_RESULT = "<h1>Title</h1>\n<p><em>italic</em> <strong>bold</strong></p>"

    assert(load_md_data('test_md') == TEST_STRING_RESULT)


def test_render_template(full_site):
    OUTPUT = f"<h1> Output </h1> {full_site.static_path} ../end.html"
    assert(render_template('template.html', string="Output") == OUTPUT)


def test_url_for(tmp_path, site):
    @site.register('path')
    def path_a():
        assert(path_a)
        assert(url_for(path_b) == 'second/path')
        assert(url_for('path_b') == 'second/path')
        assert(url_for(path_c, with_var='path') == 'third/path')
        assert(url_for('path_c', with_var='path') == 'third/path')
        with pytest.raises(RuntimeError, match='path_d'):
            url = url_for('path_d')
            url = url_for('path_d', random='variable')
        return ''

    @site.register('second/path')
    def path_b():
        assert(url_for(path_a) == '../path')
        assert(url_for('path_a') == '../path')
        assert(url_for(path_c, with_var='path') == '../third/path')
        assert(url_for('path_c', with_var='path') == '../third/path')
        return ''

    @site.register('third/<with_var>', validate=False)
    def path_c():
        assert(url_for(path_a) == '../path')
        assert(url_for('path_a') == '../path')
        assert(url_for(path_b) == '../second/path')
        assert(url_for('path_b') == '../second/path')
        assert(url_for(path_c, with_var='path') == 'path')
        assert(url_for('path_c', with_var='path') == 'path')
        return ''

    path_a()
    path_b()
    path_c()

def test_static_url(full_site):
    @full_site.register('path.html')
    def path():
        assert(static_url('static_file') == 'static/static_file')
        with pytest.warns(Warning, match='Could not find'):
            assert(static_url('fake.txt') == 'static/fake.txt')
        return ''

    path()
