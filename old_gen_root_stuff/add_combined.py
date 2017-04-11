from abc import abstractmethod

class AddCombined():
    def __init__(self, source, max_index, target):
        self._source = source
        self._max_index = max_index
        self._target = target

    @abstractmethod
    def add(self):
        pass