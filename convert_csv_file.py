from ast import literal_eval
from datetime import timedelta
from pathlib import Path
from typing import NamedTuple

import can
import pandas
import pandas as pd

from convert_trc_file import explain_msg


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


def convert_csv_file(path):
    path = Path(path)
    if not (path.exists() and path.is_file() and path.suffix == '.csv'):
        raise ValueError('Invalid path')
    with open(path.with_suffix('.txt'), mode='w') as out_file:
        df = pd.read_csv(path,
                         names=['bus', 'no', 'time', 'state', 'id', 'length', 'message', 'data', 'ascii'],
                         converters={'time': convert_time,
                                     'no': convert_no,
                                     'id': convert_id,
                                     'data': convert_data},
                         sep=';', skiprows=1)

        for i, row in df.iterrows():
            msg = can.Message(timestamp=row.time, is_fd=False, arbitration_id=row.id,
                              is_rx=False, dlc=row.length, data=row.data, is_extended_id=False)
            line = f"{row.no} {msg.timestamp:.1f} {explain_msg(msg)}\n"
            out_file.write(line)


if __name__ == "__main__":
    convert_csv_file("Trace_24-06-10_140743.csv")
    convert_csv_file("test.csv")
