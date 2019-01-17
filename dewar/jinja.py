JINJA_FUNCTIONS = []

def add_jinja_global(arg=None):
    def decorator(func):
        JINJA_FUNCTIONS.append(func)
        return func

    if callable(arg):
        return decorator(arg) # return 'wrapper'
    else:
        return decorator # ... or 'decorator'
