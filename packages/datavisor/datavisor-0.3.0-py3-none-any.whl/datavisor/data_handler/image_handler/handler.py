# src/datavisor/data_handler/image_handler/handler.py

from PIL import Image
import io
from typing import List, Optional

import os
import sys

src_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(src_path)

from datavisor.data_handler.base_handler import BaseDataHandler
from datavisor.config import ImageEntry, EntryMetadata, Config, ImageDimensions
from datavisor.config.exceptions import ProcessingError, ValidationError

class ImageHandler(BaseDataHandler):
    def __init__(self, config: Config):
        super().__init__(config)
        self.preserve_original_size = config.image_dimensions is None
        self.target_size = None if self.preserve_original_size else (config.image_dimensions.width, config.image_dimensions.height)

    def process(
        self,
        data: Optional[bytes] = None,
        original_name: Optional[str] = None,
        ocr_data: Optional[List[List[str]]] = None,
        annotations: Optional[dict] = None
    ) -> ImageEntry:
        if data is None:
            raise ValidationError("Image data cannot be None")
        if not self.validate(data):
            raise ValidationError("Invalid image data")

        try:
            # Open the image
            img = Image.open(io.BytesIO(data))

            # Store the original format
            original_format = img.format or 'PNG'

            # Always store the original dimensions
            original_dimensions = ImageDimensions(width=img.width, height=img.height)

            if self.preserve_original_size:
                img_resized = img
                final_dimensions = original_dimensions
            else:
                img_resized = img.resize(self.target_size)
                final_dimensions = self.config.image_dimensions

            # Convert back to bytes, preserving original format
            img_byte_arr = io.BytesIO()
            img_resized.save(img_byte_arr, format=original_format)
            processed_data = img_byte_arr.getvalue()

            # Extract just the file name from the path
            original_name = os.path.basename(original_name) if original_name else 'unknown'

            # Create metadata
            metadata = EntryMetadata(
                original_name=original_name,
                original_format=original_format,
                original_width=original_dimensions.width,
                original_height=original_dimensions.height,
                word_count=len(ocr_data) if ocr_data else 0
            )

            # Create and return the ImageEntry
            return ImageEntry(
                data=processed_data,
                metadata=metadata,
                dimensions=final_dimensions,
                ocr_data=ocr_data,
                annotations=annotations
            )

        except Exception as e:
            raise ProcessingError(f"Failed to process image: {str(e)}")

    def validate(self, data: Optional[bytes]) -> bool:
        if data is None:
            return False
        try:
            Image.open(io.BytesIO(data))
            return True
        except:
            return False
