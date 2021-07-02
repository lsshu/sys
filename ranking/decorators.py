from functools import wraps


def demo(*args, **kwargs):
    """修饰器"""

    def decorator(func):
        @wraps(func)
        def wrapped_function(*func_args, **func_kwargs):
            response = func(*func_args, **func_kwargs)
            return response

        return wrapped_function

    return decorator


def proxies(func):
    """修饰器"""

    @wraps(func)
    def wrapped_function(*func_args, **func_kwargs):
        response = func(*func_args, **func_kwargs)
        return response

    return wrapped_function
