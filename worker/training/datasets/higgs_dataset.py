from training.datasets.base_dataset import BaseDataset
from training.metadata.dataset_metadata import DatasetMetadata

class HiggsDataset(BaseDataset):
    def get_dataloader(self, partition_id, batch_size):
        pass
    
    def partition(self, partition_id: int, total_partitions: int, batch_size: int):
        pass

    def get_metadata(self):
        return DatasetMetadata(
            name = " Higgs",
            num_samples = 11_000_000,
            num_featurs = 28,
            num_classes = 2,
            version = "1.0"
        )
    
    def load(self):
        pass

    def downlaod_if_missing(self):
        pass