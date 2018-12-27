from collections import namedtuple
from pathlib import Path
import functools

from dewar.parser import fill_path

class Site:
    def __init__(self):
        self.registered_functions = set()

    def register(self, path):
        if path.startswith('/'):
            raise ValueError("Path argument can't begin with a '/''")
        
        def decorator(f):
            def wrapper():
                try:
                    return wrapper._returned
                except AttributeError:
                    if hasattr(wrapper, '_called'):
                        raise RuntimeError("Calling functions within themselves not allowed!")
                    else:
                        wrapper._called = True
                    val = f()
                    wrapper._returned = val
                    return val

            wrapper.name = f.__name__
            wrapper.__name__ = wrapper.name
            wrapper.path = path
            
            self.registered_functions.add(wrapper)
            return wrapper
        
        return decorator

    def _render_file(self, path, content):
        render_path_folder = path.parent
        render_path_folder.mkdir(parents=True, exist_ok=True)

        with open(path, 'w') as render_file:
            render_file.write(content)

    def render(self, path='./dist/'):
        path = Path(path)
        render_functions = self.registered_functions
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


