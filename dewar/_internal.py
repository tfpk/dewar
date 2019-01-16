import inspect
import copy
from pathlib import Path

from collections import namedtuple


def get_caller_location(frames=2):
    stack = inspect.stack()
    if len(stack) < frames:
        raise ValueError("frames argument larger than actual number of frames.")
    path = Path(stack[frames].filename)
    if path.exists():
        return path.parent.absolute()

    raise RuntimeError("Directory for caller location could not be found!")


InfoTuple = namedtuple('InfoTuple', 'function_name variables')


def _frame_info_iterator():
    init_frame = inspect.currentframe()
    frame = init_frame.f_back
    while frame:
        frame_vars = copy.copy(frame.f_globals)
        frame_vars.update(frame.f_locals)
        yield InfoTuple(inspect.getframeinfo(frame).function, frame_vars)
        frame = frame.f_back


def _hasattr_static(obj, name):
    try:
        inspect.getattr_static(obj, name)
        return True
    except AttributeError:
        return False


def get_closest_path():
    frame = inspect.currentframe()
    for frame in _frame_info_iterator():
        func = frame.variables.get(frame.function_name)
        if hasattr(func, '_registered_to'):
            return func.path
    raise RuntimeError("There is no current dewar page being loaded")


def get_closest_site():
    frame = inspect.currentframe()
    for frame in _frame_info_iterator():
        func = frame.variables.get(frame.function_name)
        # static prevents site recursing on itself when accessed
        if _hasattr_static(func, '_registered_to'):
            return func._registered_to
    raise RuntimeError("There is no current dewar site in call history.")
