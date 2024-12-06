# src/datavisor/io_ops/visor_reader.py

import os
from typing import Iterator
import json
from datavisor.config import Config, ImageDimensions
from datavisor.file_format.visor_file import VisorFile
from datavisor.config.exceptions import IOError

class VisorReader:
    def __init__(self, metadata_file: str):
        self.metadata_file = metadata_file
        self.metadata = self._load_metadata()
        self.config = self._create_config_from_metadata()
        self.files = self.metadata['files']
        self.base_dir = os.path.dirname(self.metadata_file)
        self.total_entries = self.metadata['total_entries']

    def _load_metadata(self) -> dict:
        try:
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise IOError(f"Failed to read metadata file: {str(e)}")

    def _create_config_from_metadata(self) -> Config:
        meta_config = self.metadata['config']
        image_dimensions = None
        if not meta_config['preserve_original_size'] and meta_config['image_dimensions'] is not None:
            image_dimensions = ImageDimensions(
                width=meta_config['image_dimensions']['width'],
                height=meta_config['image_dimensions']['height']
            )
        return Config(
            data_type=meta_config['data_type'],
            image_dimensions=image_dimensions,
            max_entries_per_file=meta_config['max_entries_per_file'],
            compression=meta_config.get('compression', False)
        )

    def __iter__(self) -> Iterator:
        for filename in self.files:
            filepath = os.path.join(self.base_dir, filename)
            try:
                with open(filepath, 'rb') as f:
                    for entry in VisorFile.iter_entries(f):
                        yield entry
            except Exception as e:
                print(f"Warning: Failed to read Visor file {filename}: {str(e)}")

    def __len__(self) -> int:
        return self.total_entries

    def print_summary(self):
        print(f"Dataset summary:")
        print(f"Total entries: {self.total_entries}")
        print(f"Number of .visor files: {len(self.files)}")
        if self.config.image_dimensions:
            print(f"Target image dimensions: {self.config.image_dimensions.width}x{self.config.image_dimensions.height}")
        else:
            print("Original image sizes preserved")
        print(f"Max entries per file: {self.config.max_entries_per_file}")
        print(f"Compression: {'Enabled' if self.config.compression else 'Disabled'}")
        print("\nEntries per file:")
        for filename in self.files:
            print(f"  {filename}")
