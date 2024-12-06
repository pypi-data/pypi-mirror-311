class CustomDateMismatchException(NotImplementedError):
    """Exception raised when a date's year does not match the expected value."""
    def __init__(self, actual_d, expected_min_m='3', expected_min_y='2024', expected_min_d='2'):
        message = f"Such date for currency operations is not supported by Exchange API: minimal expected data that supported by API, year: {expected_min_y}, month: {expected_min_m}, day: {expected_min_d}, but got {actual_d}."
        super().__init__(message)
        self.actual_d = actual_d
        self.expected_min_m = expected_min_m
        self.expected_min_y = expected_min_y
        self.expected_min_d = expected_min_d