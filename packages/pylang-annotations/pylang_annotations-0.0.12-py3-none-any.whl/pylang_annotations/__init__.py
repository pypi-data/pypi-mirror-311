def native(onlyFunc=None, /):
    if type(onlyFunc) is bool:
        def wrapper(func):
            return func
        return wrapper
    return onlyFunc


def pure(func, /):
    return func


skip_module: object
