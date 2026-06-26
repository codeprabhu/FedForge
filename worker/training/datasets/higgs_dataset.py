from training.datasets.base_dataset import BaseDataset
class HiggsDataset(BaseDataset):
    def get_dataloader(self, partition_id, batch_size):
        return {
            "partition_id": partition_id,
            "num_samples": batch_size
        }