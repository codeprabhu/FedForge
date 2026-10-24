import gzip
import json
from pathlib import Path

import numpy as np  # type: ignore
import pandas as pd  # type: ignore
import requests
import torch  # type: ignore
from torch.utils.data import DataLoader, TensorDataset  # type: ignore

from core.config import (HIGGS_DATALOADER_WORKERS, HIGGS_DATASET_URL,
                         HIGGS_MAX_ROWS, HIGGS_PREPROCESS_CHUNK_ROWS)
from training.datasets.base_dataset import BaseDataset
from training.metadata.dataset_metadata import DatasetMetadata
from training.storage.dataset_storage import DatasetStorage


class HiggsDataset(BaseDataset):
    """Full Higgs data with a persistent, memory-mapped worker-side cache."""

    FILE_NAME = "HIGGS.csv.gz"
    NUM_FEATURES = 28

    def __init__(self):
        self._storage = DatasetStorage("higgs")
        self._storage.initialize()
        self._manifest = None

    def _dataset_file_path(self) -> Path:
        return self._storage.raw_dir() / self.FILE_NAME

    def _open_text(self, path: Path):
        return gzip.open(path, "rt") if path.suffix == ".gz" else open(path, "r")

    def _row_count(self, path: Path) -> int:
        with self._open_text(path) as source:
            return sum(1 for _ in source)

    def _ensure_processed_cache(self):
        if self._manifest is not None:
            return self._manifest
        dataset_file = self.download_if_missing()
        manifest_path = self._storage.processed_manifest_file()
        features_path = self._storage.processed_features_file()
        labels_path = self._storage.processed_labels_file()
        source_rows = self._row_count(dataset_file)
        max_rows = source_rows if HIGGS_MAX_ROWS <= 0 else min(HIGGS_MAX_ROWS, source_rows)
        expected = {"rows": max_rows, "features": self.NUM_FEATURES,
                    "source": str(dataset_file), "max_rows": HIGGS_MAX_ROWS}
        if manifest_path.exists() and features_path.exists() and labels_path.exists():
            with manifest_path.open() as manifest_file:
                cached = json.load(manifest_file)
            if cached == expected:
                self._manifest = cached
                return cached

        features = np.lib.format.open_memmap(
            features_path, mode="w+", dtype="float32",
            shape=(expected["rows"], self.NUM_FEATURES))
        labels = np.lib.format.open_memmap(
            labels_path, mode="w+", dtype="float32", shape=(expected["rows"],))
        written = 0
        for chunk in pd.read_csv(
            dataset_file, header=None, chunksize=HIGGS_PREPROCESS_CHUNK_ROWS,
            dtype=np.float32,
        ):
            if written >= expected["rows"]:
                break
            chunk = chunk.iloc[:expected["rows"] - written]
            values = chunk.to_numpy(dtype=np.float32, copy=False)
            end = written + len(values)
            labels[written:end] = values[:, 0]
            features[written:end] = values[:, 1:]
            written = end
        if written != expected["rows"]:
            raise RuntimeError(f"HIGGS row count changed during preprocessing: {written} != {expected['rows']}")
        features.flush()
        labels.flush()
        del features, labels
        with manifest_path.open("w") as manifest_file:
            json.dump(expected, manifest_file)
        self._manifest = expected
        return expected

    def _partition_bounds(self, partition_id: int, total_partitions: int):
        if total_partitions < 1 or not 0 <= partition_id < total_partitions:
            raise ValueError("partition_id must be in [0, total_partitions)")
        rows = self._ensure_processed_cache()["rows"]
        return rows * partition_id // total_partitions, rows * (partition_id + 1) // total_partitions

    def get_dataloader(self, partition_id: int, total_partitions: int, batch_size: int):
        if batch_size < 1:
            raise ValueError("batch_size must be positive")
        start, end = self._partition_bounds(partition_id, total_partitions)
        features = np.load(self._storage.processed_features_file(), mmap_mode="r")
        labels = np.load(self._storage.processed_labels_file(), mmap_mode="r")
        feature_tensor = torch.from_numpy(np.asarray(features[start:end]))
        label_tensor = torch.from_numpy(np.asarray(labels[start:end]))
        loader = DataLoader(
            TensorDataset(feature_tensor, label_tensor), batch_size=batch_size, shuffle=True,
            num_workers=HIGGS_DATALOADER_WORKERS,
            pin_memory=torch.cuda.is_available(),
            persistent_workers=HIGGS_DATALOADER_WORKERS > 0,
        )
        return loader, end - start

    def partition(self, partition_id: int, total_partitions: int):
        start, end = self._partition_bounds(partition_id, total_partitions)
        features = np.load(self._storage.processed_features_file(), mmap_mode="r")
        labels = np.load(self._storage.processed_labels_file(), mmap_mode="r")
        return pd.DataFrame(np.column_stack((labels[start:end], features[start:end])))

    def get_metadata(self):
        return DatasetMetadata(name="Higgs", num_samples=self._ensure_processed_cache()["rows"],
                               num_features=self.NUM_FEATURES, num_classes=2, version="1.0",
                               download_url=HIGGS_DATASET_URL)

    def load(self):
        self._ensure_processed_cache()
        return self.partition(0, 1)

    def download_if_missing(self):
        dataset_file = self._dataset_file_path()
        legacy_file = self._storage.raw_dir() / "HIGGS.csv"
        if legacy_file.exists():
            return legacy_file
        if dataset_file.exists():
            return dataset_file
        response = requests.get(HIGGS_DATASET_URL, stream=True, timeout=120)
        response.raise_for_status()
        with dataset_file.open("wb") as output:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    output.write(chunk)
        return dataset_file
