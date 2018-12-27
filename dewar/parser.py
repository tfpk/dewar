import re
from collections import OrderedDict

def parse_path(path):
    """
    Given a path formatted like /<category>/<page>.html, will return ['category', 'page']
    """
    if not isinstance(path, str):
        raise TypeError("Path can't be processed - not a string.")
    
    path_re = r'\<.*?\>'
    tokens = re.findall(path_re, path)
    tokens = map(lambda x: x.replace('<', '').replace('>', ''), tokens)

    return list(OrderedDict.fromkeys(tokens))
    
def fill_path(path, params):
    path_elems = parse_path(path)
    if isinstance(params, str):
        params = tuple([params])

    for elem, param in zip(path_elems, params):
        path = path.replace(f'<{elem}>', param)

    return path
