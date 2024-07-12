import argparse
from pathlib import Path

import can

from custom_log_reader import CustomLogReader
from custom_log_writer import CustomLogWriter

parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='*', type=argparse.FileType('r'))
args = parser.parse_args()

if not args.files:
    print('KMCANverbose file1.trc file2.csv')

for file in args.files:
    in_path = Path(file.name)
    with CustomLogReader(in_path) as reader:
        out_path = in_path.with_suffix('.txt')
        print(f'Writing from {file.name} to {out_path}')
        with CustomLogWriter(str(out_path)) as writer:
            for msg in reader:
                msg: can.Message
                writer.on_message_received(msg)
