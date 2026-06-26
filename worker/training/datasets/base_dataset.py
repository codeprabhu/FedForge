from abc import ABC, abstractmethod
from training.metadata.dataset_metadata import DatasetMetadata

class BaseDataset(ABC):
    @abstractmethod
    def get_dataloader(self, partition_id: int,total_partition: int, batch_size: int):
        pass

    @abstractmethod
    def get_metadata(self) -> DatasetMetadata:
        pass

    @abstractmethod 
    def partition(self, partition_id: int, total_partition: int):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def downlaod_if_missing(self):
        pass