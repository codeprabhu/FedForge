from pathlib import Path
class DatasetsPaths:
    ROOT_DIR = Path("worker_data")

    def __init__(self, dataset_name: str):
        self._dataset_name = dataset_name

    def dataset_dir(self) -> Path:
        return (self.ROOT_DIR/"datasets"/self._dataset_name)
    
    def raw_dir(self) -> Path:
        return self.dataset_dir()/"raw"

    def processed_dir(self) -> Path:
        return self.dataset_dir()/"processed"
    
    def metadata_file(self) -> Path:
        return self.dataset_dir()/"metadata.json"