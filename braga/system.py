import abc
import threading

from braga.aspect import Aspect


class System(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, aspect=None):
        self.thread = None
        self.aspect = aspect if aspect else Aspect()

    def start(self):
        self.thread = threading.Thread(name=type(self).__name__, target=self.update)
        self.thread.start()

    @abc.abstractmethod
    def update(self):
        """Updates the entities in this system"""
