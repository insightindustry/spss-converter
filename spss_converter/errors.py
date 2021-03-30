class SPSSConverterError(ValueError):
    """Base exception raised by the **SPSS Converter** library."""
    pass


class ColumnNameNotFoundError(ValueError):
    """Exception raised when a given column or variable name is not found."""
    pass


class InvalidDataFormatError(ValueError):
    """Exception raised when a value did not conform to an expected type."""
    pass


class InvalidLayoutError(ValueError):
    """Exception raised when a layout value was not recognized."""
    pass
