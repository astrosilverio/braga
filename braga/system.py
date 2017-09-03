import functools


def call_hooks(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        run_hooks(function.system, function.__name__, 'before', *args, **kwargs)
        result = function(*args, **kwargs)
        run_hooks(function.system, function.__name__, 'after', *args, **kwargs)
        return result

    wrapper.__wrapped__ = function
    return wrapper


class System(object):
    """Handler for modifying and updating Entities with a particular pattern of Components."""

    def __init__(self, world=None):
        if world:
            self.world = world

    def __call__(self, func):
        setattr(func, 'system', self)
        wrapped_func = call_hooks(func)
        setattr(self, func.__name__, wrapped_func)
        return wrapped_func


def run_hooks(system, function_name, position, *fn_args, **fn_kwargs):
    if hasattr(system, 'world'):
        callbacks = system.world.subscriptions[system][function_name][position]
        for callback in callbacks:
            callback(*fn_args, **fn_kwargs)
