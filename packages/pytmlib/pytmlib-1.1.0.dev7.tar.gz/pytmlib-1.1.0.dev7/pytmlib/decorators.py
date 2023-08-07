import functools

ENTRYPOINT_MARKER = '__pytm_entrypoint__'


def entrypoint(func):
    setattr(func, ENTRYPOINT_MARKER, True)

    @functools.wraps(func)
    def decorator(*args, **kwargs):
        return func(*args, **kwargs)

    return func
