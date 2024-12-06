# src/datavisor/file_format/visor_file.py

import io
import struct
import os
import sys

from typing import Optional, Iterator
from .visor_header import VisorHeader
from .visor_entry import VisorEntry
from datavisor.config import Config
from datavisor.config.exceptions import IOError

class VisorFile:
    def __init__(self, config: Config, file_path: str):
        self.config = config
        self.file_path = file_path
        self.file_obj = open(file_path, 'wb')
        self.header = None
        self.entry_count = 0
        self.image_dimensions = config.image_dimensions
        self.metadata_size = 0  # Currently not used

        # Write a placeholder for the header
        self.header_size = VisorHeader.size()
        self.file_obj.write(b'\0' * self.header_size)
        self.file_obj.flush()

    def add_entry(self, entry):
        # Write the entry to the file
        visor_entry = VisorEntry(entry)
        entry_data = visor_entry.pack()
        self.file_obj.write(entry_data)
        self.file_obj.flush()
        self.entry_count += 1

    def finalize(self):
        # Now that all entries are written, we can write the header
        self.file_obj.seek(0)
        self.header = VisorHeader(
            image_dimensions=self.image_dimensions,
            entry_count=self.entry_count,
            metadata_size=self.metadata_size
        )
        self.file_obj.write(self.header.pack())
        self.file_obj.flush()
        self.file_obj.close()

    @classmethod
    def iter_entries(cls, file_obj: io.IOBase) -> Iterator:
        # Read and unpack header
        header_data = file_obj.read(VisorHeader.size())
        header = VisorHeader.unpack(header_data)

        # Iterate over entries
        for _ in range(header.entry_count):
            entry_header_size = struct.calcsize(VisorEntry.ENTRY_FORMAT)
            entry_header = file_obj.read(entry_header_size)
            if not entry_header or len(entry_header) < entry_header_size:
                print("Warning: Incomplete entry header encountered.")
                break

            # Unpack entry header to determine sizes
            sizes = struct.unpack(VisorEntry.ENTRY_FORMAT, entry_header)
            data_size, metadata_size, ocr_data_size, annotations_size, _, _, entry_type = sizes

            total_entry_size = entry_header_size + data_size + metadata_size + ocr_data_size + annotations_size
            # Move back to start of entry
            file_obj.seek(-entry_header_size, io.SEEK_CUR)
            entry_data = file_obj.read(total_entry_size)
            entry = VisorEntry.unpack(entry_data)
            yield entry
