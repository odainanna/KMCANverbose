from pathlib import Path

from convert_csv_file import convert_csv_file
from convert_trc_file import convert_trc_file


def convert(path):
    path = Path(path)
    if not path.is_file() and path.exists():
        raise ValueError("File not found")
    if path.suffix == '.trc':
        convert_trc_file(path)
    elif path.suffix == '.csv':
        convert_csv_file(path)
    else:
        raise ValueError('Unsupported format')


if __name__ == '__main__':
        convert('tests/15_05_02.17.trc')
        convert('Trace_24-06-10_140743.csv')
        convert('test.csv')