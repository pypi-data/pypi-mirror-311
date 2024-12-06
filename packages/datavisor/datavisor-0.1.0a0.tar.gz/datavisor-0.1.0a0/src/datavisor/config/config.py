from dataclasses import dataclass
from typing import List, Union, Optional 

@dataclass
class ImageDimensions:
    width: int
    height: int

    def validate(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Width and height must be positive integers")

@dataclass
class Config:
    """Configuration class for Visor library."""
    data_type: str  # 'image' or 'text'
    max_entries_per_file: int  # Maximum number of entries per .visor file
    image_dimensions: Optional[ImageDimensions] = None  # Dimensions for resizing images, None to preserve original size
    compression: bool = False  # Whether to use compression
    cache_size: int = 100  # Number of entries to cache

    def validate(self):
        """Validate the configuration."""
        if self.data_type not in ['image', 'text']:
            raise ValueError("data_type must be either 'image' or 'text'")
        if self.image_dimensions is not None:
            self.image_dimensions.validate()
        if self.max_entries_per_file <= 0:
            raise ValueError("max_entries_per_file must be positive")
        if not isinstance(self.compression, bool):
            raise ValueError("compression must be a boolean")
        if self.cache_size < 0:
            raise ValueError("cache_size must be non-negative")

@dataclass
class EntryMetadata:
    """Metadata for each entry in the Visor file."""
    original_name: str
    original_format: str
    original_width: int
    original_height: int
    word_count: int

    def validate(self):
        """Validate the metadata."""
        if not isinstance(self.original_name, str) or not self.original_name:
            raise ValueError("original_name must be a non-empty string")
        if not isinstance(self.original_format, str) or not self.original_format:
            raise ValueError("original_format must be a non-empty string")
        if self.original_width <= 0 or self.original_height <= 0:
            raise ValueError("original_width and original_height must be positive integers")
        if self.word_count < 0:
            raise ValueError("word_count must be a non-negative integer")
        
@dataclass
class Entry:
    """Represents an entry in the Visor file."""
    data: bytes  # The actual image data
    metadata: EntryMetadata
    dimensions: ImageDimensions
    ocr_data: List[List[Union[str, List[float]]]]  # List of words, each word is a list containing text and potentially bbox

    def validate(self):
        """Validate the entry."""
        if not isinstance(self.data, bytes):
            raise ValueError("data must be bytes")
        self.metadata.validate()
        self.dimensions.validate()
        if not isinstance(self.ocr_data, list):
            raise ValueError("ocr_data must be a list")
        for word in self.ocr_data:
            if not isinstance(word, list) or len(word) < 1:
                raise ValueError("Each item in ocr_data must be a non-empty list")
            if not isinstance(word[0], str):
                raise ValueError("The first item of each word in ocr_data must be a string")