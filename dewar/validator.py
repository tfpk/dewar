from dewar.exceptions import ValidationError
from dewar.parser import parse_path


def validate_page(func):
    def validate_dict(val, path_elements, func_name):
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
            error_text = ": Page's return contained strings as keys, when it needed multiple variables."
            raise ValidationError(func_name + error_text)

        if not all(map(is_correct_size, val)):
            error_text = ": Page's return contained incorrect number of variables for path."
            raise ValidationError(func_name + error_text)

        return True

    """Given a page function which returned a value.
    
    :param val: the return from `func`
    :type val: str, dict

    :param func: the function that's being used
    :type func: function

    :return: Whether or not the return value given is valid
    :rtype: bool
    """
    name = func.name
    path = func.path
    val = func()
    path_elements = parse_path(path)
    if type(val) is str:
        if path_elements:
            raise ValidationError(f"{name}'s path requires variables, which were not provided.")
    elif type(val) is dict:
        if len(path_elements) == 0:
            error_text = "{name}'s path did not specify variables, but returned variables anyway."
            raise ValidationError(error_text)
        validate_dict(val, path_elements, name)
    else:
        raise ValidationError(f"{name} did not return a valid object to construct the page.")

    return True
