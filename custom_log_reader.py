from abc import ABC
from pathlib import Path
from typing import Union, TextIO, Generator, Any

from can.io.generic import MessageReader
from can.typechecking import StringPathLike

from custom_csv_reader import CustomCSVReader
from custom_trc_reader import CustomTRCReader


class CustomLogReader(MessageReader, ABC):
    def __new__(self, file: Union[StringPathLike, TextIO]):
        path = Path(file)
        dct = {'.trc': CustomTRCReader, '.csv': CustomCSVReader}
        if path.suffix in dct:
            return dct[path.suffix](file)
        else:
            return ValueError('Invalid path')