from exceptions.unknown_dataset_error import UnknownDatasetError

class DatasetRegistry:
    def __init__(self):
        self._datasets = {}

    def register(self, name:str, dataset_class):
        if name in self._datasets:
            raise ValueError(f"Dataset {name} already Registered.")
        
        self._datasets[name] = dataset_class

    def get(self, name: str):
        dataset_class = self._datasets.get(name)

        if dataset_class is None:
            raise UnknownDatasetError(name)
        
        return dataset_class