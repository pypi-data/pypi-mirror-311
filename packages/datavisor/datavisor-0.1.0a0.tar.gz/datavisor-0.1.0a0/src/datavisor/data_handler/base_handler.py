from abc import ABC, abstractmethod

import os
import sys

src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(src_path)

from config import Entry, Config

class BaseDataHandler(ABC):
    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    def process(self, data: bytes) -> Entry:
        """
        Process the input data and return an Entry object.
        """
        pass

    @abstractmethod
    def validate(self, data: bytes) -> bool:
        """
        Validate the input data.
        """
        pass