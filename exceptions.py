"""Кастомные исключения"""


class NotSendingError(Exception):
    """События, которые не пересылаются в Telegram"""

    def __init__(self, message):
        self.message = message


class SendingError(NotSendingError):
    """События уровня Error, которые будут пересылаться в Telegram"""

    pass
