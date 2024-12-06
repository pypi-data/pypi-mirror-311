# src/datavisor/io_ops/visor_writer.py

import os
import json
from typing import List
from datavisor.config import Config
from datavisor.file_format.visor_file import VisorFile
from datavisor.config.exceptions import IOError

class VisorWriter:
    def __init__(self, config: Config, output_dir: str):
        self.config = config
        self.output_dir = output_dir
        self.current_file_index = 0
        self.total_entries = 0
        self.files_written = []
        self._ensure_output_dir_exists()
        self.current_visor_file = None

    def _ensure_output_dir_exists(self):
        try:
            os.makedirs(self.output_dir, exist_ok=True)
        except Exception as e:
            raise IOError(f"Failed to create output directory: {str(e)}")

    def write_entries(self, entries: List):
        for entry in entries:
            if self.current_visor_file is None:
                # Start a new file
                filename = f"visor_data_{self.current_file_index}.visor"
                filepath = os.path.join(self.output_dir, filename)
                self.current_visor_file = VisorFile(self.config, filepath)
                self.files_written.append(filename)

            self.current_visor_file.add_entry(entry)
            self.total_entries += 1

            if self.current_visor_file.entry_count >= self.config.max_entries_per_file:
                # Finalize current file
                self.current_visor_file.finalize()
                self.current_file_index += 1
                self.current_visor_file = None

        # Finalize any remaining file
        if self.current_visor_file is not None:
            self.current_visor_file.finalize()
            self.current_file_index += 1
            self.current_visor_file = None

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
        self.total_entries = 0
        self.files_written = []
