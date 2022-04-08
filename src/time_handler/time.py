"""Houses the classes that handle time and time conversions"""
from datetime import datetime

class TimeStringConverter:
    """A class for converting datetime objects to strings and vice versa
    Attributes:
        time_string_format: The default format used for conversions.
                            Refer to datetime documentation for format codes."""

    def __init__(self, time_string_format: str):
        """Create a new TimeStringConverter
        Args:
            time_string_format: The desired format used for conversions.
                                Refer to datetime documentation for format codes."""

        self.time_string_format = time_string_format

    def datetime_to_string(self, datetime_obj: datetime, time_string_format=None):
        """Convert a datetime object to string
        Args:
            datetime_obj: The datetime object to convert
            time_string_format: The format according to which things will be converted
        Returns: A string representation of the datetime object"""

        if not time_string_format:
            time_string_format = self.time_string_format
        return datetime.strftime(datetime_obj, time_string_format)

    def string_to_datetime(self, datetime_str: str, time_string_format=None):
        """Convert a string to a datetime object
        Args:
            datetime_str: The string to be converted
            time_string_format: The format according to which things will be converted
        Returns: A datetime object equal to the string representation"""

        if not time_string_format:
            time_string_format = self.time_string_format
        return datetime.strptime(datetime_str, time_string_format)

class TimeDifference:
    """A class for calculating time differences between two times"""

    def time_difference_ms(self, first_datetime: datetime, second_datetime: datetime):
        """Get the time difference between two dates and times in milliseconds
        first_datetime - second_datetime
        Args:
            first_datetime: The first datetime for the comparison
            second_datetime: The second datetime for the comparison
        Returns: The time difference in milliseconds.
                 The value is negative if the latter datetime comes after the first."""

        time_multiplier = 1
        if first_datetime < second_datetime:
            delta = second_datetime - first_datetime
            time_multiplier = -1
        else:
            delta = first_datetime - second_datetime
        time_ms = delta.days * 24 * 60 * 60 * 1000 + \
                      delta.seconds * 1000 + \
                      delta.microseconds / 1000
        return time_multiplier * round(time_ms)
