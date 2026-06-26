from abc import ABC, abstractmethod
class BaseDataset(ABC):
    @abstractmethod
    def get_dataloader(self, partition_id: int, batch_size: int):
        pass