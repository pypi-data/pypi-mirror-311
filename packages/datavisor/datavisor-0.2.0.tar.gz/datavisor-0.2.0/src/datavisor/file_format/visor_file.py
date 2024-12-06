# src/datavisor/file_format/visor_file.py

import io
import struct

import os
import sys 

src_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(src_path)

from typing import List, Iterator
from .visor_header import VisorHeader
from .visor_entry import VisorEntry
from datavisor.config import Config

class VisorFile:
    def __init__(self, config: Config):
        self.config = config
        self.header = None
        self.entries = []

    def add_entry(self, entry):
        if len(self.entries) >= self.config.max_entries_per_file:
            raise ValueError("Maximum number of entries reached for this file")
        self.entries.append(entry)

    def write(self, file_obj: io.IOBase):
        # Calculate metadata size (assume it's constant for all entries)
        metadata_size = 0  # Not used in this context

        # Create and write header
        self.header = VisorHeader(self.config.image_dimensions, len(self.entries), metadata_size)
        file_obj.write(self.header.pack())

        # Write entries
        for entry in self.entries:
            file_obj.write(VisorEntry(entry).pack())

    @classmethod
    def read(cls, file_obj: io.IOBase, config: Config) -> 'VisorFile':
        visor_file = cls(config)

        # Read and unpack header
        header_data = file_obj.read(VisorHeader.size())
        visor_file.header = VisorHeader.unpack(header_data)

        # Read entries
        while True:
            entry_header_size = struct.calcsize(VisorEntry.ENTRY_FORMAT)
            entry_header = file_obj.read(entry_header_size)
            if not entry_header:
                break  # End of file

            # Unpack entry header to determine sizes
            sizes = struct.unpack(VisorEntry.ENTRY_FORMAT, entry_header)
            data_size, metadata_size, ocr_data_size, _, entry_type = sizes

            total_entry_size = entry_header_size + data_size + metadata_size + ocr_data_size
            file_obj.seek(-entry_header_size, io.SEEK_CUR)

            entry_data = file_obj.read(total_entry_size)
            entry = VisorEntry.unpack(entry_data)
            visor_file.entries.append(entry)

        return visor_file

    def __iter__(self) -> Iterator:
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)
