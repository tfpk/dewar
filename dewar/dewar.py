from collections import namedtuple
from pathlib import Path
import functools

class Site:
    def __init__(self):
        self.registered_functions = set()

    def register(self, path):
        def decorator(f):
            def wrapper():
                try:
                    return wrapper._returned
                except AttributeError:
                    val = f()
                    wrapper._returned = val
                    return val

            wrapper.name = f.__name__
            wrapper.__name__ = wrapper.name
            wrapper.path = path
            wrapper.real_func = f
            
            self.registered_functions.add(wrapper)
            return wrapper
        
        return decorator

    def render(self, path='./dist/'):
        path = Path(path)
        render_functions = self.registered_functions
        for func in render_functions:
            val = func()
            render_path = path / func.path

            render_path_folder = render_path.parent
            render_path_folder.mkdir(parents=True, exist_ok=True)

            with open(render_path, 'w') as render_file:
                render_file.write(func())

