from dataclasses import dataclass

@dataclass
class DatasetMetadata:
    name: str
    num_samples: str
    num_features: int | None
    num_classes: int | None
    version: str

    download_url: str