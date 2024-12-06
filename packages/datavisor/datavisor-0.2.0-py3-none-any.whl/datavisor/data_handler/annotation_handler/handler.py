# src/datavisor/data_handler/annotations_handler/handler.py

from typing import Optional

import os
import sys

src_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(src_path)

from datavisor.data_handler.base_handler import BaseDataHandler
from datavisor.config import AnnotEntry, Config
from datavisor.config.exceptions import ProcessingError, ValidationError

class AnnotationHandler(BaseDataHandler):
    def __init__(self, config: Config):
        super().__init__(config)

    def process(self, annotation_data: dict, ocr_data: Optional[dict] = None) -> AnnotEntry:
        if not self.validate(annotation_data):
            raise ValidationError("Invalid annotation data")

        try:
            # Create and return the AnnotEntry
            return AnnotEntry(annotation=annotation_data, ocr_data=ocr_data)

        except Exception as e:
            raise ProcessingError(f"Failed to process annotation: {str(e)}")

    def validate(self, data: dict) -> bool:
        if not isinstance(data, dict):
            return False
        # Additional validation logic can be added here
        return True
