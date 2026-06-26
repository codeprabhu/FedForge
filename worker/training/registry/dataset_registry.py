from exceptions.unknown_dataset_error import UnknownDatasetError

class DatasetRegistry:
    def __init__(self):
        self._datasets = {}

    def register(self, name, dataset_class):
        self._datasets[name] = dataset_class

    def get(self, name):
        if name not in self._datasets:
            raise UnknownDatasetError("Unknown Dataset: {name}")
        
        return self._datasets[name]