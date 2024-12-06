import io
import struct

import os
import sys 

src_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(src_path)

from typing import List, Iterator
from .visor_header import VisorHeader
from .visor_entry import VisorEntry
from config import Entry, Config

class VisorFile:
    def __init__(self, config: Config):
        self.config = config
        self.header = None
        self.entries = []

    def add_entry(self, entry: Entry):
        if len(self.entries) >= self.config.max_entries_per_file:
            raise ValueError("Maximum number of entries reached for this file")
        self.entries.append(entry)

    def write(self, file_obj: io.IOBase):
        # Calculate metadata size (assume it's constant for all entries)
        metadata_size = VisorEntry.size(self.entries[0]) - len(self.entries[0].data) - struct.calcsize(VisorEntry.ENTRY_FORMAT)

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
        for _ in range(visor_file.header.entry_count):
            entry_data = file_obj.read(struct.calcsize(VisorEntry.ENTRY_FORMAT))
            image_data_size, metadata_size, ocr_data_size, _ = struct.unpack(VisorEntry.ENTRY_FORMAT, entry_data)
            
            total_entry_size = struct.calcsize(VisorEntry.ENTRY_FORMAT) + image_data_size + metadata_size + ocr_data_size
            file_obj.seek(-struct.calcsize(VisorEntry.ENTRY_FORMAT), io.SEEK_CUR)
            
            entry_data = file_obj.read(total_entry_size)
            entry = VisorEntry.unpack(entry_data)
            visor_file.entries.append(entry)

        return visor_file

    def __iter__(self) -> Iterator[Entry]:
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)