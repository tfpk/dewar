from collections import namedtuple
from pathlib import Path

import functools
import shutil
import time

from proxy_tools import module_property

from dewar.jinja import JINJA_FUNCTIONS
from dewar.parser import fill_path
from dewar.validator import validate_page
from dewar._internal import get_caller_location, get_closest_site

from jinja2 import Environment, FileSystemLoader, select_autoescape


@module_property
def site():
    """The site property returns an instance of a site.

    It first searches the stack to find the most recent function
    registered to a site. If it finds one, it returns that site.

    If it can't find a site in the stack, it returns the most
    recently created site instance.

    Otherwise, it raises a RuntimeError.
    """
    try:
        return get_closest_site()
    except RuntimeError:
        pass

    if '_site_instances' in globals():
        return _site_instances[-1]
    raise RuntimeError("Site could not be found.")


class Site:
    """This is the root class of any dewar project, that encapsulates
    all the pages in a project.

    :param path: the path where the directories with site files can
                 be found, such as the `templates/` and `static/`
                 directories.
    """

    def __init__(self, path=None, create_backups=True):
        self.registered_functions = set()
        self.create_backups = create_backups

        if path:
            self.path = Path(path)
        else:
            self.path = get_caller_location()

        self.template_path = self.path / 'templates'
        self.static_path = self.path / 'static'

        self._jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_path), followlinks=True),
            autoescape=select_autoescape(['html', 'xml'])
        )
        for func in JINJA_FUNCTIONS:
            self._jinja_env.globals[func.__name__] = func
        self._jinja_env.globals['site'] = self

        if '_site_instances' not in globals():
            global _site_instances
            _site_instances = []
        _site_instances.append(self)

    def register(self, path, validate=True):
        """A decorator that registers a page function with a site.

        :param path: The path to that page in the rendered site.
        :param validate: If True, when the page function returns,
                         it will raise an error if it doesn't return
                         a value that can create a page/pages.
        """
        if path.startswith('/'):
            raise ValueError("Path argument can't begin with a '/''")

        def decorator(f):
            def wrapper():
                if hasattr(wrapper, '_returned'):
                    return wrapper._returned
                elif hasattr(wrapper, '_called'):
                    raise RuntimeError("Calling functions within themselves not allowed!")
                else:
                    wrapper._called = True

                content = f()
                wrapper._returned = content
                if validate:
                    validate_page(wrapper)
                return content

            wrapper.name = f.__name__
            wrapper.__name__ = wrapper.name
            wrapper.path = path
            wrapper._registered_to = self

            self.registered_functions.add(wrapper)
            return wrapper

        return decorator

    def close(self):
        """Remove a site from the global list of sites.

        This functionality is rarely needed, as most applications will
        only involve one site. If you need it though, this will prevent
        this module's site property from returning returning this site.

        Note: The site property will still return this site if it is
        used in a page function registered to this site, or by a
        function that is called by a page function registered to
        this site.
        """
        try:
            _site_instances.remove(self)
        except ValueError:
            raise RuntimeError("Site Instance was already closed.")

    def _render_file(self, path, content):
        """Renders a given file to a path. Used by the render function.

        :param path: a path to write to.
        :param content: content to be written to that path.

        """
        render_path_folder = path.parent
        render_path_folder.mkdir(parents=True, exist_ok=True)

        with open(path, 'w') as render_file:
            render_file.write(content)

    def _render_static(self, path):
        """Renders all the static content to the given path

        :param path: The path to write to.
        """
        static_render_path = path / 'static'
        if not self.static_path.exists():
            return
        shutil.copytree(self.static_path, static_render_path)

    def render(self, path='./dist/'):
        """Write the site to a path.

        :param path: The path to write to.
        """
        path = Path(path)
        render_functions = self.registered_functions
        if self.create_backups:
            shutil.make_archive(path / '..' / 'old' / f'site_{time.time()}', 'zip', path)
        shutil.rmtree(path)
        self._render_static(path)
        for func in render_functions:
            content = func()
            if isinstance(content, str):
                render_path = path / func.path
                self._render_file(render_path, content)
            else:
                for params in content:
                    filled_path = fill_path(func.path, params)
                    render_path = path / filled_path
                    self._render_file(render_path, content[params])

