class VisorException(Exception):
    """Base exception class for Visor library."""

class ConfigurationError(VisorException):
    """Raised when there's an error in the configuration."""

class ProcessingError(VisorException):
    """Raised when there's an error during data processing."""

class IOError(VisorException):
    """Raised when there's an input/output error."""

class ValidationError(VisorException):
    """Raised when there's a validation error."""