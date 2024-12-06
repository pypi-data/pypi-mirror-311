# src/datavisor/io_ops/visor_writer.py

import os
import json
from typing import List

import os
import sys

src_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(src_path)

from config import Config, ImageEntry, AnnotEntry
from file_format import VisorFile
from config.exceptions import IOError

class VisorWriter:
    def __init__(self, config: Config, output_dir: str):
        self.config = config
        self.output_dir = output_dir
        self.current_file_index = 0
        self.current_visor_file = VisorFile(config)
        self.total_entries = 0
        self.files_written = []
        self._ensure_output_dir_exists()

    def _ensure_output_dir_exists(self):
        try:
            os.makedirs(self.output_dir, exist_ok=True)
        except Exception as e:
            raise IOError(f"Failed to create output directory: {str(e)}")

    def write_entries(self, entries: List):
        for entry in entries:
            if len(self.current_visor_file) >= self.config.max_entries_per_file:
                self._write_current_file()
                self.current_file_index += 1
                self.current_visor_file = VisorFile(self.config)

            self.current_visor_file.add_entry(entry)
            self.total_entries += 1

        # Write any remaining entries
        if len(self.current_visor_file) > 0:
            self._write_current_file()

    def _write_current_file(self):
        filename = f"visor_data_{self.current_file_index}.visor"
        filepath = os.path.join(self.output_dir, filename)

        try:
            with open(filepath, 'wb') as f:
                self.current_visor_file.write(f)
            self.files_written.append(filename)
        except Exception as e:
            raise IOError(f"Failed to write Visor file: {str(e)}")

    def finalize(self):
        # Write a metadata file with information about the dataset
        metadata = {
            'total_entries': self.total_entries,
            'files': self.files_written,
            'config': {
                'data_type': self.config.data_type,
                'preserve_original_size': self.config.image_dimensions is None,
                'image_dimensions': None if self.config.image_dimensions is None else {
                    'width': self.config.image_dimensions.width,
                    'height': self.config.image_dimensions.height
                },
                'max_entries_per_file': self.config.max_entries_per_file,
                'compression': self.config.compression
            }
        }

        metadata_file = os.path.join(self.output_dir, 'visor_metadata.json')
        try:
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            raise IOError(f"Failed to write metadata file: {str(e)}")

        print(f"Finalized writing {self.total_entries} entries across {len(self.files_written)} files.")
        print(f"Metadata written to {metadata_file}")

        # Reset the writer state
        self.current_file_index = 0
        self.current_visor_file = VisorFile(self.config)
        self.total_entries = 0
        self.files_written = []
