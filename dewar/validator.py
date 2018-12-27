from dewar.exceptions import ValidationError
from dewar.parser import parse_path

def validate_dict(val, path_elements, func_name):
    """
    Given a dict which was returned from a registered page, check it's valid given that page's path.
    """
    def has_correct_type(key):
        "Return if key is of correct type"
        return isinstance(key, tuple) or isinstance(key, str)

    def is_allowed_single(key):
        "Return, if key is string, whether it is allowed to be a string"
        return len(path_elements) == 1 or isinstance(key, tuple)

    def is_correct_size(key):
        "Return, if key is a tuple, whether it has the right number of parts"
        return len(key) == len(path_elements) or isinstance(key, str)
   

    if not all(map(has_correct_type, val)):
        raise ValidationError(func_name + ": Page's return did not contain keys of the right type.")

    if not all(map(is_allowed_single, val)):
        raise ValidationError(func_name + ": Page's return contained strings as keys, when page required multiple variables.")

    if not all(map(is_correct_size, val)):
        raise ValidationError(func_name + ": Page's return contained incorrect number of variables for path.")

    return True


def validate_page(val, func):
    name = func.name
    path = func.path
    path_elements = parse_path(path)
    if str(val) == val:
        if path_elements:
            raise ValidationError(f"{name}'s path requires variables, which were not provided.")
    elif type(val) is dict:
        if len(path_elements) == 0:
            raise ValidationError("{name}'s path did not specify variables, but returned variables anyway.")
        validate_dict(val, path_elements, name)
    else:
        raise ValidationError(f"{name} did not return a valid object to construct the page.")

    return True

