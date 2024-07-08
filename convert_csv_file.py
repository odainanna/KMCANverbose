from ast import literal_eval
from datetime import timedelta
from pathlib import Path

import can
import pandas
import pandas as pd

from convert_trc_file import explain_msg


def convert_to_timedelta(abs_time):
    seconds, milliseconds, microseconds, nanoseconds = map(float, abs_time.split('.'))
    microseconds += milliseconds * 1000 + nanoseconds // 1000
    t = timedelta(seconds=seconds, microseconds=microseconds)
    return t


def time_to_timestamp(abs_time):
    t = convert_to_timedelta(abs_time)
    return float(f'{t.seconds}.{t.microseconds}')


def recreate_message(x):
    timestamp = time_to_timestamp(x.time_abs)
    is_fd = False
    try:
        arbitration_id = literal_eval('0x' + x.id_hex)
    except SyntaxError:
        arbitration_id = -1  # todo: Error is an option
    is_rx = False
    dlc = x.length
    if pandas.notna(x.data_hex):
        data = bytearray(x.data_hex, 'utf8')
    else:
        data = None
    return can.Message(timestamp=timestamp, is_fd=is_fd, arbitration_id=arbitration_id,
                       is_rx=is_rx, dlc=dlc, data=data, is_extended_id=False)


def convert_csv_file_to_out_file(path):
    path = Path(path)
    if not path.exists():
        raise ValueError(f'{path} does not exist')
    elif not (path.is_file() and path.suffix == '.csv'):
        raise ValueError(f'{path} should be a .csv-file')
    out_path = Path(path).with_suffix('.txt')
    with open(out_path, mode='w') as out_file:
        # Read the CSV file
        df = pd.read_csv(path, sep=';')

        # Change the columns
        df.columns = ['bus', 'no', 'time_abs', 'state', 'id_hex', 'length', 'message', 'data_hex', 'ascii']

        for i, row in df.iterrows():
            msg = recreate_message(row)
            line = f"{i + 1} {msg.timestamp:.1f} {explain_msg(msg)}".strip() + "\n"
            out_file.write(line)

    return out_path


if __name__ == "__main__":
    convert_csv_file_to_out_file("Trace_24-06-10_140743.csv")
