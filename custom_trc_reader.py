from datetime import timedelta
from typing import TextIO, Union, Any, Generator

import can
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


def parse_trc_line(line):
    """
    :param line: str like "      1      1453.159 FD     0716 Rx 1  05 "
    :return: line_nr, the line converted to a can.Message object
    """
    parts = line.split()
    try:
        line_nr = int(parts[0])
        timestamp = float(parts[1])
        is_fd = parts[2] == 'FD'
        is_dt = parts[2] == 'DT'
        is_st = parts[2] == 'ST'
        if is_fd or is_dt:
            arbitration_msg_id = int(parts[3], 16)  # Convert hex to int
            is_rx = parts[4] == 'Rx'
            dlc = int(parts[5])
            data = [int(x, 16) for x in parts[6:]]  # Convert hex to int and put in a list
        elif is_st:
            arbitration_msg_id = -1  # the id slot is missing
            is_rx = parts[3] == 'Rx'
            dlc = int(parts[4])
            data = [int(x, 16) for x in parts[5:]]  # Convert hex to int and put in a list
        else:
            raise ValueError(f'Failed to parse {line}')
        return line_nr, can.Message(timestamp=timestamp, is_fd=is_fd, arbitration_id=arbitration_msg_id,
                                    is_rx=is_rx, dlc=dlc, data=data, is_extended_id=False)
    except IndexError:
        raise ValueError(f'Failed to parse {line}')


class CustomTRCReader(MessageReader):
    """Iterator over CAN messages from a .csv file."""

    file: TextIO

    def __init__(
            self,
            file: Union[StringPathLike, TextIO],
            **kwargs: Any,
    ) -> None:
        """
        :param file: a path-like object or as file-like object to read from
        """
        super().__init__(file, mode="r")

    def __iter__(self) -> Generator[Message, None, None]:
        for line in self.file:
            msg = self.string_to_message(line)
            if msg is None:
                continue
            yield msg
        self.stop()

    @staticmethod
    def string_to_message(line):
        try:
            line_nr, msg = parse_trc_line(line)
        except Exception as e:
            return None
        return msg
