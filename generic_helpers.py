def is_var_number(var):
    try:
        return type(var) == int or type(var) == float
    except Exception:
        pass
    return False

def is_var_function(var):
    try:
        return callable(var)
    except Exception:
        pass
    return False