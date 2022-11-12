def is_var_number(var) -> bool:
    try:
        return type(var) == int or type(var) == float #pylint: disable=unidiomatic-typecheck
    except Exception:
        pass
    return False

def is_var_function(var) -> bool:
    try:
        return callable(var)
    except Exception:
        pass
    return False
