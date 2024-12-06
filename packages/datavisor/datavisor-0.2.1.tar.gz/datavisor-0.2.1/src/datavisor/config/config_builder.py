# src/datavisor/config/config_builder.py

from .config import Config, ImageDimensions
from .exceptions import ConfigurationError

class ConfigBuilder:
    """Builder class for creating Config objects."""

    def __init__(self):
        self._data_type = None
        self._image_dimensions = None
        self._max_entries_per_file = None
        self._compression = False
        self._cache_size = 100

    def set_data_type(self, data_type: str):
        if data_type not in ['image', 'text', 'annotation']:
            raise ValueError("data_type must be 'image', 'text', or 'annotation'")
        self._data_type = data_type
        return self

    def set_image_dimensions(self, width: int, height: int):
        self._image_dimensions = ImageDimensions(width, height)
        return self

    def set_max_entries_per_file(self, max_entries: int):
        self._max_entries_per_file = max_entries
        return self

    def set_compression(self, compression: bool):
        self._compression = compression
        return self

    def set_cache_size(self, cache_size: int):
        self._cache_size = cache_size
        return self

    def build(self) -> Config:
        if not all([self._data_type, self._max_entries_per_file]):
            raise ConfigurationError("Missing required configuration parameters")

        config = Config(
            data_type=self._data_type,
            image_dimensions=self._image_dimensions,
            max_entries_per_file=self._max_entries_per_file,
            compression=self._compression,
            cache_size=self._cache_size
        )

        try:
            config.validate()
        except ValueError as e:
            raise ConfigurationError(str(e))

        return config
