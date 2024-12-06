# src/datavisor/file_format/visor_entry.py

import struct
import os
import sys
import json

src_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(src_path)

from datavisor.config import ImageEntry, AnnotEntry, EntryMetadata, ImageDimensions

# Define constants for entry types
ENTRY_TYPE_IMAGE = 1
ENTRY_TYPE_ANNOT = 2

class VisorEntry:
    ENTRY_FORMAT = '<IIIIIIi'  # Sizes and entry type

    def __init__(self, entry):
        self.entry = entry
        if isinstance(entry, ImageEntry):
            self.entry_type = ENTRY_TYPE_IMAGE
        elif isinstance(entry, AnnotEntry):
            self.entry_type = ENTRY_TYPE_ANNOT
        else:
            raise ValueError("Unsupported entry type")

    def pack(self) -> bytes:
        if self.entry_type == ENTRY_TYPE_IMAGE:
            # For ImageEntry
            data = self.entry.data or b''
            data_size = len(data)
            metadata_dict = {}
            if self.entry.metadata:
                metadata_dict = {
                    'original_name': self.entry.metadata.original_name,
                    'original_format': self.entry.metadata.original_format,
                    'original_width': self.entry.metadata.original_width,
                    'original_height': self.entry.metadata.original_height,
                    'word_count': self.entry.metadata.word_count,
                }
            if self.entry.dimensions:
                metadata_dict['dimensions'] = {
                    'width': self.entry.dimensions.width,
                    'height': self.entry.dimensions.height
                }
            metadata_json = json.dumps(metadata_dict).encode()
            metadata_size = len(metadata_json)
            ocr_data_json = json.dumps(self.entry.ocr_data).encode() if self.entry.ocr_data else b''
            ocr_data_size = len(ocr_data_json)
            annotations_json = json.dumps(self.entry.annotations).encode() if self.entry.annotations else b''
            annotations_size = len(annotations_json)
        elif self.entry_type == ENTRY_TYPE_ANNOT:
            # For AnnotEntry
            data_json = json.dumps(self.entry.annotation).encode() if self.entry.annotation else b''
            data = data_json
            data_size = len(data_json)
            metadata_json = b''  # No metadata
            metadata_size = 0
            ocr_data_json = json.dumps(self.entry.ocr_data).encode() if self.entry.ocr_data else b''
            ocr_data_size = len(ocr_data_json)
            annotations_json = b''
            annotations_size = 0
        else:
            raise ValueError("Unsupported entry type")

        packed = struct.pack(
            self.ENTRY_FORMAT,
            data_size,
            metadata_size,
            ocr_data_size,
            annotations_size,
            0,  # padding
            0,  # additional padding
            self.entry_type
        )
        packed += data
        packed += metadata_json
        packed += ocr_data_json
        packed += annotations_json
        return packed

    @classmethod
    def unpack(cls, data: bytes):
        header_size = struct.calcsize(cls.ENTRY_FORMAT)
        sizes = struct.unpack(cls.ENTRY_FORMAT, data[:header_size])
        data_size, metadata_size, ocr_data_size, annotations_size, _, _, entry_type = sizes

        offset = header_size

        data_bytes = data[offset:offset+data_size]
        offset += data_size

        metadata_bytes = data[offset:offset+metadata_size]
        offset += metadata_size

        ocr_data_bytes = data[offset:offset+ocr_data_size]
        offset += ocr_data_size

        annotations_bytes = data[offset:offset+annotations_size]
        offset += annotations_size

        if entry_type == ENTRY_TYPE_IMAGE:
            # For ImageEntry
            metadata_dict = json.loads(metadata_bytes) if metadata_bytes else {}
            ocr_data = json.loads(ocr_data_bytes) if ocr_data_bytes else None
            annotations = json.loads(annotations_bytes) if annotations_bytes else None
            metadata = EntryMetadata(
                original_name=metadata_dict.get('original_name', 'unknown'),
                original_format=metadata_dict.get('original_format', 'unknown'),
                original_width=metadata_dict.get('original_width', 0),
                original_height=metadata_dict.get('original_height', 0),
                word_count=metadata_dict.get('word_count', 0)
            ) if metadata_dict else None
            dimensions = ImageDimensions(
                width=metadata_dict.get('dimensions', {}).get('width', 0),
                height=metadata_dict.get('dimensions', {}).get('height', 0)
            ) if 'dimensions' in metadata_dict else None
            entry = ImageEntry(
                data=data_bytes if data_bytes else None,
                metadata=metadata,
                dimensions=dimensions,
                ocr_data=ocr_data,
                annotations=annotations
            )
        elif entry_type == ENTRY_TYPE_ANNOT:
            # For AnnotEntry
            annotation = json.loads(data_bytes) if data_bytes else None
            ocr_data = json.loads(ocr_data_bytes) if ocr_data_bytes else None
            entry = AnnotEntry(
                annotation=annotation,
                ocr_data=ocr_data
            )
        else:
            raise ValueError("Unknown entry type")

        return entry

    @classmethod
    def size(cls, entry):
        if isinstance(entry, ImageEntry):
            data_size = len(entry.data) if entry.data else 0
            metadata_dict = {}
            if entry.metadata:
                metadata_dict = {
                    'original_name': entry.metadata.original_name,
                    'original_format': entry.metadata.original_format,
                    'original_width': entry.metadata.original_width,
                    'original_height': entry.metadata.original_height,
                    'word_count': entry.metadata.word_count,
                }
            if entry.dimensions:
                metadata_dict['dimensions'] = {
                    'width': entry.dimensions.width,
                    'height': entry.dimensions.height
                }
            metadata_json = json.dumps(metadata_dict).encode()
            metadata_size = len(metadata_json)
            ocr_data_json = json.dumps(entry.ocr_data).encode() if entry.ocr_data else b''
            ocr_data_size = len(ocr_data_json)
            annotations_json = json.dumps(entry.annotations).encode() if entry.annotations else b''
            annotations_size = len(annotations_json)
        elif isinstance(entry, AnnotEntry):
            data_json = json.dumps(entry.annotation).encode() if entry.annotation else b''
            data_size = len(data_json)
            metadata_size = 0
            ocr_data_size = len(json.dumps(entry.ocr_data).encode()) if entry.ocr_data else 0
            annotations_size = 0
        else:
            raise ValueError("Unsupported entry type")

        return (
            struct.calcsize(cls.ENTRY_FORMAT) +
            data_size +
            metadata_size +
            ocr_data_size +
            annotations_size
        )
