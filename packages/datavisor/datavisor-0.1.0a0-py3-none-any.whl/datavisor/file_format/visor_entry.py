import struct
import os
import sys
import json

src_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(src_path)

from config import Entry, EntryMetadata, ImageDimensions

class VisorEntry:
    ENTRY_FORMAT = '<IIII'  # Size of image data, metadata size, ocr_data size, padding (for future use)

    def __init__(self, entry: Entry):
        self.entry = entry

    def pack(self) -> bytes:
        image_data_size = len(self.entry.data)
        metadata_dict = {
            'original_name': self.entry.metadata.original_name,
            'original_format': self.entry.metadata.original_format,
            'original_width': self.entry.metadata.original_width,
            'original_height': self.entry.metadata.original_height,
            'word_count': self.entry.metadata.word_count,
            'dimensions': {
                'width': self.entry.dimensions.width,
                'height': self.entry.dimensions.height
            }
        }
        metadata_json = json.dumps(metadata_dict).encode()
        metadata_size = len(metadata_json)
        ocr_data_json = json.dumps(self.entry.ocr_data).encode()
        ocr_data_size = len(ocr_data_json)

        packed = struct.pack(
            self.ENTRY_FORMAT,
            image_data_size,
            metadata_size,
            ocr_data_size,
            0  # padding for future use
        )
        packed += self.entry.data
        packed += metadata_json
        packed += ocr_data_json
        return packed

    @classmethod
    def unpack(cls, data: bytes) -> Entry:
        header_size = struct.calcsize(cls.ENTRY_FORMAT)
        image_data_size, metadata_size, ocr_data_size, _ = struct.unpack(cls.ENTRY_FORMAT, data[:header_size])
        
        image_data = data[header_size:header_size+image_data_size]
        metadata_json = data[header_size+image_data_size:header_size+image_data_size+metadata_size]
        ocr_data_json = data[header_size+image_data_size+metadata_size:header_size+image_data_size+metadata_size+ocr_data_size]
        
        metadata_dict = json.loads(metadata_json)
        ocr_data = json.loads(ocr_data_json)
        
        metadata = EntryMetadata(
            original_name=metadata_dict['original_name'],
            original_format=metadata_dict['original_format'],
            original_width=metadata_dict['original_width'],
            original_height=metadata_dict['original_height'],
            word_count=metadata_dict['word_count']
        )
        dimensions = ImageDimensions(
            width=metadata_dict['dimensions']['width'],
            height=metadata_dict['dimensions']['height']
        )
        return Entry(data=image_data, metadata=metadata, dimensions=dimensions, ocr_data=ocr_data)

    @classmethod
    def size(cls, entry: Entry) -> int:
        metadata_dict = {
            'original_name': entry.metadata.original_name,
            'original_format': entry.metadata.original_format,
            'original_width': entry.metadata.original_width,
            'original_height': entry.metadata.original_height,
            'word_count': entry.metadata.word_count,
            'dimensions': {
                'width': entry.dimensions.width,
                'height': entry.dimensions.height
            }
        }
        metadata_json = json.dumps(metadata_dict).encode()
        ocr_data_json = json.dumps(entry.ocr_data).encode()
        return (
            struct.calcsize(cls.ENTRY_FORMAT) +
            len(entry.data) +
            len(metadata_json) +
            len(ocr_data_json)
        )