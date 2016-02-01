class Component(object):
    """Base class to be inherited by user-defined Component types."""

    INITIAL_PROPERTIES = []

    def __repr__(self):
        return type(self).__name__
