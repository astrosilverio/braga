import abc
from functools import wraps

from braga.aspect import Aspect


def call_hooks(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        run_hooks(args[0], function.__name__, 'before', *args, **kwargs)
        result = function(*args, **kwargs)
        run_hooks(args[0], function.__name__, 'after', *args, **kwargs)

        return result

    wrapper.__wrapped__ = function
    return wrapper


class System(object):
    """Handler for modifying and updating Entities with a particular pattern of Components."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, world, aspect=None):
        self.world = world
        self.aspect = aspect if aspect else Aspect()

    def __new__(cls, *args, **kwargs):
        for name, obj in vars(cls).items():
            if callable(obj) and not name.startswith('_') and not hasattr(obj, '__wrapped__'):
                try:
                    obj = obj.__func__
                except AttributeError:
                    pass
                setattr(cls, name, call_hooks(obj))
        new_system = object.__new__(cls, *args, **kwargs)
        return new_system

    def __contains__(self, entity):
        return entity in self.aspect

    @property
    def entities(self):
        """Set of Entities in the World with this Aspect"""
        return self.world.entities_with_aspect(self.aspect)

    @abc.abstractmethod
    def update(self):
        """Updates the entities in this system"""


def run_hooks(system, function_name, position, *fn_args, **fn_kwargs):
    callbacks = system.world.subscriptions[system][function_name][position]
    for callback in callbacks:
        callback(*fn_args, **fn_kwargs)
