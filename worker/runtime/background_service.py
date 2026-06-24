from abc import ABC, abstractmethod

class BackgroundService(ABC):
    @abstractmethod
    def run(self, *args):
        pass

    @abstractmethod
    def stop(self):
        pass