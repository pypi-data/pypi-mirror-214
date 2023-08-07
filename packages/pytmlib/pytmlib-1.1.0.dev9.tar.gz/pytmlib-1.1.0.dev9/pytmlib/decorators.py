import functools

ENTRYPOINT_MARKER = '__pytm_entrypoint__'
ENTRYPOINT_TITLE = '__pytm_entrypoint_title__'


def entrypoint(func_or_title):
    if isinstance(func_or_title, str):
        def wrapper(func):
            setattr(func, ENTRYPOINT_MARKER, True)
            setattr(func, ENTRYPOINT_TITLE, func_or_title)

            @functools.wraps(func)
            def inner(*args, **kwargs):
                return func(*args, **kwargs)

            return inner

        return wrapper
    else:
        setattr(func_or_title, ENTRYPOINT_MARKER, True)

        @functools.wraps(func_or_title)
        def outer(*args, **kwargs):
            return func_or_title(*args, **kwargs)

        return outer
