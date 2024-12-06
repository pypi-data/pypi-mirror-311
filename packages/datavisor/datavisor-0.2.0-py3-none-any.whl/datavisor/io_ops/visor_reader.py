# src/datavisor/io_ops/visor_reader.py

import os
from typing import List, Iterator, Optional

import os
import sys
import json

src_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(src_path)

from config import Config, ImageEntry, AnnotEntry, ImageDimensions
from file_format import VisorFile
from config.exceptions import IOError

class VisorReader:
    def __init__(self, metadata_file: str):
        self.metadata_file = metadata_file
        self.metadata = self._load_metadata()
        self.config = self._create_config_from_metadata()
        self.visor_files = self._load_visor_files()
        self.total_entries = sum(len(vf) for vf in self.visor_files)

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

    def _load_visor_files(self) -> List[VisorFile]:
        visor_files = []
        base_dir = os.path.dirname(self.metadata_file)
        for filename in self.metadata['files']:
            filepath = os.path.join(base_dir, filename)
            try:
                with open(filepath, 'rb') as f:
                    visor_files.append(VisorFile.read(f, self.config))
            except Exception as e:
                print(f"Warning: Failed to read Visor file {filename}: {str(e)}")
        if not visor_files:
            print(f"Warning: No valid .visor files found in metadata")
        return visor_files

    def __iter__(self) -> Iterator:
        for visor_file in self.visor_files:
            yield from visor_file

    def __len__(self) -> int:
        return self.total_entries

    def get_entry(self, index: int) -> Optional:
        if index < 0 or index >= self.total_entries:
            return None

        current_index = 0
        for visor_file in self.visor_files:
            if current_index + len(visor_file) > index:
                return visor_file.entries[index - current_index]
            current_index += len(visor_file)
        return None

    def get_metadata(self, index: int) -> Optional[dict]:
        entry = self.get_entry(index)
        if entry is None:
            return None
        if isinstance(entry, ImageEntry):
            return {
                'original_name': entry.metadata.original_name,
                'original_format': entry.metadata.original_format,
                'original_width': entry.metadata.original_width,
                'original_height': entry.metadata.original_height,
                'word_count': entry.metadata.word_count,
                'dimensions': (entry.dimensions.width, entry.dimensions.height),
            }
        elif isinstance(entry, AnnotEntry):
            return {
                'annotation_keys': list(entry.annotation.keys()),
                'ocr_data_present': entry.ocr_data is not None
            }

    def print_summary(self):
        print(f"Dataset summary:")
        print(f"Total entries: {self.total_entries}")
        print(f"Number of .visor files: {len(self.visor_files)}")
        if self.config.image_dimensions:
            print(f"Target image dimensions: {self.config.image_dimensions.width}x{self.config.image_dimensions.height}")
        else:
            print("Original image sizes preserved")
        print(f"Max entries per file: {self.config.max_entries_per_file}")
        print(f"Compression: {'Enabled' if self.config.compression else 'Disabled'}")
        print("\nEntries per file:")
        for filename, visor_file in zip(self.metadata['files'], self.visor_files):
            print(f"  {filename}: {len(visor_file)} entries")
