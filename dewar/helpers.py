from pathlib import Path
from os.path import relpath

from dewar import dewar, site
from dewar.jinja import add_jinja_global
from dewar.parser import fill_path, parse_path
from dewar._internal import get_closest_path
import json
import warnings

from markdown import markdown

# anything -> final return
WRAPPER = """
<!doctype html>

<html lang="en"> <head> <meta charset="utf-8">
</head>
<body>
{content}
</body>
</html>
"""


def add_wrapper(content, wrapper=WRAPPER):
    """Add a basic HTML template around some given text.

    :param content: The HTML to fill in.
    :type content: str
    :param wrapper: A string that contains '{content}'.
    :type wrapper: str

    :returns: the wrapped content.
    :rtype: str
    """
    return wrapper.format(content=content)


def render_template(template, **kwargs):
    """Given a path to a template, and arguments to fill in,
    render that template.
    
    :param template: a path to a jinja template (relative to the 
                     template directory.)
    :type template: path.Pathlib, str

    :param keywords: the variables to be set as the context for the jinja
                   template.
    """
    template = site._jinja_env.get_template(template)
    return template.render(**kwargs)

# load from saved directories


DATA = 'data'


def load_data(path):
    """Load the text of a data file at a path

    :param path: the path of the data file, relative to the 
                 data directory of the site.
    :type path: str or pathlib.Path

    :returns: the text of the data.
    :rtype: str

    """
    data_path = dewar.site.path / DATA / Path(path)
    if not data_path.is_file():
        raise ValueError('The given path is not a file.')
    return data_path.read_text()


def load_data_dir(path):
    """Load the text of every file in the data directory.

    :param path: the path of the data directory, relative to the 
                 data directory of the site.
    :type path: str or pathlib.Path

    :returns: a dictionary of 'file_name': 'text in file' 
    :rtype: dict

    """
    data_path = dewar.site.path / DATA / Path(path)
    if not data_path.is_dir():
        raise ValueError('The given path is not a directory.')
    return {
        str(p.relative_to(data_path)): p.read_text()
        for p in data_path.iterdir()
        if p.is_file()
    }


# interpret data
def load_json(data):
    """Load json from text
    
    :param data: the text of some data
    :type data: str
    
    :returns: a dictionary that matches the json found in the text.
    :rtype: dict
    """
    return json.loads(data)


def load_json_data(path):
    """Load json from a path
    
    :param path: the path to some data (relative to a site's data dir)
    :type data: pathlib.Path or str
    
    :returns: a dictionary that matches the json found at the path.
    :rtype: dict
    """
    return load_json(load_data(path))


def load_md(data):
    """Load markdown into html from text
    
    :param data: the text of some data
    :type data: str
    
    :returns: a string with html that represents the markdown in a path.
    :rtype: dict
    """
    return markdown(data)


def load_md_data(path):
    """Load md into html from a path
    
    :param path: the path to some data (relative to a site's data dir)
    :type data: pathlib.Path or str
    
    :returns: a string with html that represents the markdown in the file.
    :rtype: str
    """
    return load_md(load_data(path))

# links


FILL_VARS_WITH = 'xUNFILLED_VARx'
@add_jinja_global
def rel_url_to(path, start=None):
    """Given a path, return a link from the current site to that path.
    
    This uses `get_closest_path()` to find the starting point if 
    start is None.
    
    :param path: the path to link to.
    :type path: pathlib.Path or str

    :param start: The path to start from (a directory, not a file),
                  or the closest path in the stack if None).
    :type start: pathlib.Path or str
    
    :returns: A relative path from `start` to `path`
    :rtype: str
    """
    if start is None:
        start = get_closest_path()
        num_path_elems = len(parse_path(start))

        start = fill_path(start, [FILL_VARS_WITH]*num_path_elems)
        start = Path(start).parent

    return relpath(path, start=start)


@add_jinja_global
def url_for(function, start=None, **kwargs):
    """Given a function (that takes `kwargs` as arguments), returns
    the relative path from start to the output of that function.
    
    This uses `get_closest_path()` to find the starting point if 
    start is None.
    
    :param function: The page function to link to, or its name.
    :type function: function, str

    :param start: The path to start from, (or the closest path in the
                  the stack if None).
    :type start: pathlib.Path, str

    :param kwargs: the arguments to `function`.

    :returns: A relative path from `start` to `path`
    :rtype: str
    """
    path = None
    if isinstance(function, str):
        for func in site.registered_functions:
            if func.name == function:
                path = func.path
                break
        else:
            raise RuntimeError(f"Could not find page function named '{function}'")
    else:
        path = function.path

    return rel_url_to(fill_path(path, kwargs.values()), start=start)


@add_jinja_global
def static_url(path, start=None):
    """Given a path relative to the static folder, return a path
    relative to the current function
    
    This will raise a warning if the static file doesn't exist.

    :param path: the path to link to (relative to the static folder).
    :type path: pathlib.Path or str

    :param start: The path to start from, (or the closest path in the
                  the stack if None).
    :type start: pathlib.Path or str
    
    :returns: A relative path from `start` to `path`
    :rtype: str
    """
    if not (site.static_path / Path(path)).is_file():
        warnings.warn(Warning('Could not find the path given.'))
    return rel_url_to('static/' + path, start=start)


kwd_mark = (object(),)


def freeze_func(arg=None):
    """A decorator for a function, that causes it to return the same
    result every time it's called (given the same arguments).

    >>> @freeze_func()
    >>> def f()
    >>>     f.num += 1
    >>>     return f.num
    >>> f.num = 0
    >>> f()
    1
    >>> f()
    1
    >>> f.num
    2
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # key function taken from functools.lru_cache()
            key = args + kwd_mark + tuple(sorted(kwargs.items()))

            if key in wrapper._returned:
                return wrapper._returned[key]

            val = func(*args, **kwargs)

            wrapper._returned[key] = val

            return val
        wrapper._returned = {}
        return wrapper

    # works both as @freeze_func, @freeze_func()
    if callable(arg):
        return decorator(arg)
    return decorator

