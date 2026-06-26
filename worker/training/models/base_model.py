from abc import ABC, abstractmethod
class BaseModel(ABC):
    @abstractmethod
    def build(self):
        pass