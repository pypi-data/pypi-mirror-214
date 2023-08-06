import logging
import datetime

class TimestampFormatter(logging.Formatter):

    """
    Formatter for timestamps
    """

    def format(self, record):
        record.asctime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return super().format(record)