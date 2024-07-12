from datetime import timedelta
from typing import TextIO, Union, Any, Generator

import pandas
from can import Message
from can.io.generic import MessageReader
from can.typechecking import StringPathLike


def convert_time(time):
    seconds, milliseconds, microseconds, nanoseconds = map(float, time.split('.'))
    microseconds += milliseconds * 1000 + nanoseconds // 1000
    t = timedelta(seconds=seconds, microseconds=microseconds)
    return t.total_seconds()


def convert_id(s):
    if s == 'Error':
        return -1  # todo
    return int(s, 16)


def convert_no(x):
    return int(x.replace('.', ''))


def convert_data(x):
    if pandas.notna(x):
        try:
            return [int(x, 16) for x in x.split()]
        except ValueError:
            return []
    return x


class CustomCSVReader(MessageReader):
    """Iterator over CAN messages from a .csv file."""

    file: TextIO

    def __init__(
            self,
            file: Union[StringPathLike, TextIO],
            **kwargs: Any,
    ) -> None:
        """
        :param file: a path-like object or as file-like object to read from
                     If this is a file-like object, is has to opened in text
                     read mode, not binary read mode.
        """
        super().__init__(file, mode="r")

    def __iter__(self) -> Generator[Message, None, None]:
        # skip the header line
        try:
            next(self.file)
        except StopIteration:
            # don't crash on a file with only a header
            return  # todo: return empty generator

        for line in self.file:
            msg = self.read_line(line)
            if msg is None:
                continue  # todo: handle errors?
            yield msg

        self.stop()

    @staticmethod
    def read_line(line):
        try:
            bus, no, time, state, id, length, message, data, ascii = line.replace('\"', '').split(';')
        except ValueError:
            return None
        return Message(
            timestamp=float(convert_time(time)),
            is_remote_frame=False,
            is_extended_id=False,
            is_error_frame=False,
            arbitration_id=convert_id(id),
            dlc=int(length),
            data=convert_data(data))