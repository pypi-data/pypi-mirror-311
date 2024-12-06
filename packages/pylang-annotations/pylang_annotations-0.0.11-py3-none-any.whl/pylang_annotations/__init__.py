def native(onlyFunc=False, /):
    def wrapper(func):
        return func
    return wrapper


def pure(func, /):
    return func


skip_module: object
