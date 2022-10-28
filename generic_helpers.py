def is_var_number(var):
    try:
        return type(var) == int or type(var) == float
    except:
        pass
    return False

def is_var_function(var):
    try:
        return callable(var)
    except:
        pass
    return False