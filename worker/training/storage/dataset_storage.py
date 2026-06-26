from training.storage.dataset_paths import DatasetsPaths

class DatasetStorage:
    def __init__(self, dataset_name: str):
        self._paths = DatasetsPaths(dataset_name)

    def initialize(self):
        self._paths.raw_dir().mkdir(parents = True, exist_ok= True)
        self._paths.processed_dir().mkdir(parents = True, exist_ok= True)

    def dataset_dir(self):
        return self._paths.dataset_dir()
    
    def raw_dir(self):
        return self._paths.raw_dir()
    
    def processed_dir(self):
        return self._paths.processed_dir()
    
    def metadata_file(self):
        return self._paths.metadata_file()