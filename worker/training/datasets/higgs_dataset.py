from training.datasets.base_dataset import BaseDataset
from training.metadata.dataset_metadata import DatasetMetadata
from training.storage.dataset_storage import DatasetStorage
import torch # type: ignore
from torch.utils.data import TensorDataset, DataLoader # type: ignore
from core.config import HIGGS_DATASET_URL, HIGGS_SAMPLE_LIMIT
from pathlib import Path
import pandas as pd # type: ignore 
import requests
class HiggsDataset(BaseDataset):
    FILE_NAME = "HIGGS.csv"

    def __init__(self):
        self._storage = DatasetStorage("higgs")
        self._storage.initialize()
        self._dataframe = None

    def _dataset_file_path(self)-> Path:
        return self._storage.raw_dir()/self.FILE_NAME

    def get_dataloader(self, partition_id: int, total_partitions: int, batch_size: int):
        partition = self.partition(partition_id,total_partitions)
        labels = partition.iloc[:, 0]
        features = partition.iloc[:, 1:]
        features = features.to_numpy()
        labels = labels.to_numpy()
        features = torch.tensor(features, dtype=torch.float32)
        labels = torch.tensor(labels, dtype=torch.float32)

        dataset = TensorDataset(features,labels)
        dataloader = DataLoader(dataset, batch_size = batch_size, shuffle = True)
        return dataloader, len(dataset)

    def partition(self, partition_id: int, total_partitions: int):
        dataframe = self.load()
        dataframe = dataframe.sample(frac = 1, random_state=42).reset_index(drop=True)
        partition_size = len(dataframe)// total_partitions
        start = partition_id * partition_size
        end = start + partition_size
        if(partition_id == total_partitions -1):
            end = len(dataframe)
        partition = dataframe.iloc[start:end]
        return partition.reset_index(drop= True)

    def get_metadata(self):
        return DatasetMetadata(
            name = " Higgs",
            num_samples = 11_000_000,
            num_features = 28,
            num_classes = 2,
            version = "1.0",
            download_url= HIGGS_DATASET_URL
        )
    
    def load(self):
        if self._dataframe is not None:
            return self._dataframe
        dataset_file = self.download_if_missing()
        self._dataframe = pd.read_csv(dataset_file, header=None, nrows=HIGGS_SAMPLE_LIMIT)
        print(f"loaded {len(self._dataframe)} samples")
        return self._dataframe

    def download_if_missing(self):
        dataset_file = self._dataset_file_path()
        if dataset_file.exists():
            print(
                f"HIGGS dataset already exists"
                f"{dataset_file}"
            )
            return dataset_file
        
        print("Downloading Higgs dataset")
        response = requests.get(HIGGS_DATASET_URL, stream= True)
        response.raise_for_status()

        with open(dataset_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Dataset Downloaded to" f"{dataset_file}")
        return dataset_file