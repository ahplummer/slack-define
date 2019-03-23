from abc import ABC, abstractmethod

class AbstractBacking(ABC):

    def __init__(self, filename):
        self._filename = filename
        super().__init__()

    @abstractmethod
    def getSpecialDefinition(self, word):
        pass

    @abstractmethod
    def addSpecialDefinition(self, word, definition):
        pass

    @abstractmethod
    def deleteSpecialDefinition(self, word):
        pass