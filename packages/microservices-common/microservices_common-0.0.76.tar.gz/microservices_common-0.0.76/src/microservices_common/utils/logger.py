import os
import logging

# Configure the logging module
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
                    level=logging.DEBUG)


class Logger:
    def __init__(self):
        pass

    @classmethod
    def format_message(cls, message, logging_info=None):
        formatted_message = "{} {}"
        return formatted_message.format(logging_info if logging_info else "", message)

    @classmethod
    def info(cls, message, logging_info=None):
        message_to_print = cls.format_message(message, logging_info)
        logging.info(message_to_print)

    @classmethod
    def error(cls, message, logging_info=None):
        message_to_print = cls.format_message(message, logging_info)
        logging.error(message_to_print)

    @classmethod
    def warning(cls, message, logging_info=None):
        message_to_print = cls.format_message(message, logging_info)
        logging.warning(message_to_print)
