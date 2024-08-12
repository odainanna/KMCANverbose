from typing import TextIO, Union, Any

from can import Message
from can.io.generic import FileIOMessageWriter
from can.typechecking import StringPathLike

from describe_message import describe_message


class CustomLogWriter(FileIOMessageWriter):
    file: TextIO

    def __init__(
            self,
            file: Union[StringPathLike, TextIO],
            append: bool = False,
            **kwargs: Any,
    ) -> None:
        """
        :param file: a path-like object or a file-like object to write to.
        :param bool append: if set to `True` messages are appended to
                            the file and no header line is written, else
                            the file is truncated and starts with a newly
                            written header line
        """
        mode = "a" if append else "w"
        super().__init__(file, mode=mode)

    def on_message_received(self, msg: Message) -> None:
        self.file.write(self.message_to_string(msg))
        self.file.write("\n")

    @staticmethod
    def message_to_string(msg: Message):
        timestamp = f'{msg.timestamp:.1f}'
        data = f'<{' '.join(f"{x:02x}" for x in msg.data)}>'
        cob_id = hex(msg.arbitration_id)
        return " ".join(
            [
                timestamp,
                cob_id,
                data,
                describe_message(msg),
            ]
        )
