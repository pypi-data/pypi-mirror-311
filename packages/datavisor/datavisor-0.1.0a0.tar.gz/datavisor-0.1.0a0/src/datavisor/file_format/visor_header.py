import struct

import os
import sys

src_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(src_path)

from config import ImageDimensions

from typing import Optional

class VisorHeader:
    MAGIC_NUMBER = b'VISOR'
    VERSION = 1
    HEADER_FORMAT = '<5sIIIIII'  # Magic number, Version, Preserve original size, Image width, Image height, Entry count, Metadata size

    def __init__(self, image_dimensions: Optional[ImageDimensions], entry_count: int, metadata_size: int):
        self.preserve_original_size = image_dimensions is None
        self.image_dimensions = image_dimensions
        self.entry_count = entry_count
        self.metadata_size = metadata_size

    def pack(self) -> bytes:
        width = 0 if self.preserve_original_size else self.image_dimensions.width
        height = 0 if self.preserve_original_size else self.image_dimensions.height
        return struct.pack(
            self.HEADER_FORMAT,
            self.MAGIC_NUMBER,
            self.VERSION,
            int(self.preserve_original_size),
            width,
            height,
            self.entry_count,
            self.metadata_size
        )

    @classmethod
    def unpack(cls, data: bytes) -> 'VisorHeader':
        unpacked = struct.unpack(cls.HEADER_FORMAT, data)
        if unpacked[0] != cls.MAGIC_NUMBER:
            raise ValueError("Invalid Visor file: Incorrect magic number")
        if unpacked[1] != cls.VERSION:
            raise ValueError(f"Unsupported Visor file version: {unpacked[1]}")
        preserve_original_size = bool(unpacked[2])
        image_dimensions = None if preserve_original_size else ImageDimensions(width=unpacked[3], height=unpacked[4])
        return cls(
            image_dimensions=image_dimensions,
            entry_count=unpacked[5],
            metadata_size=unpacked[6]
        )

    @classmethod
    def size(cls) -> int:
        return struct.calcsize(cls.HEADER_FORMAT)