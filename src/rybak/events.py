import logging
from pathlib import PurePath


class EventSink:
    def writing_file(self, template: PurePath, target: PurePath) -> None:
        """Called when TreeRenderer is about to write to a file."""

    def unlinking_file(self, target: PurePath) -> None:
        """Called when TreeRenderer is about to delete a file."""


class LoggingEventSink(EventSink):
    def __init__(self, logger: logging.Logger, level: int) -> None:
        self._logger = logger
        self._level = level

    def writing_file(self, template: PurePath, target: PurePath) -> None:
        self._logger.log(self._level, 'Render from %s to %s', template, target)

    def unlinking_file(self, target: PurePath) -> None:
        self._logger.log(self._level, 'Unlink %s', target)
