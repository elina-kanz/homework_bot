"""Кастомные исключения."""


class NotSendingError(Exception):
    """События, которые не пересылаются в Telegram."""


class SendingError(NotSendingError):
    """События уровня Error, которые будут пересылаться в Telegram."""

    pass
