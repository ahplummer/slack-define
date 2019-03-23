from abc import ABC, abstractmethod
from pylogger import projectLogger

class AbstractBacking(ABC):

    def __init__(self, filename):
        self.log = projectLogger()
        self._filename = filename
        super().__init__()

    @abstractmethod
    def getSpecialDefinition(self, word):
        self.log.debug(word + " is being retrieved.")

    @abstractmethod
    def addSpecialDefinition(self, word, definition):
        self.log.debug(word + " is being added.")

    @abstractmethod
    def deleteSpecialDefinition(self, word):
        self.log.debug(word + " is being deleted.")