from io import StringIO

import can

from custom_csv_reader import CustomCSVReader

def test_init():
    reader = CustomCSVReader(StringIO())
    assert isinstance(reader, CustomCSVReader)


def test_iter():
    reader = CustomCSVReader(StringIO(""""Bus";"No";"Time (abs)";"State";"ID (hex)";"Length";"Message";"Data (hex)";"ASCII"
"-Bus 0-";"1";"9712.036.108.4";"     ";"7E5";"8";"";"4C 00 00 00 00 00 00 00";"L......."
"-Bus 1-";"2";"9712.036.121.4";"     ";"7E5";"8";"";"4C 00 00 00 00 00 00 00";"L......."
"""))
    messages = list(reader)
    assert all(isinstance(msg, can.Message) for msg in messages)
    assert len(messages) == 2
    expected = [can.Message(timestamp=9712.036108, arbitration_id=0x7e5, is_extended_id=False, dlc=8,
                            data=[0x4c, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]),
                can.Message(timestamp=9712.036121, arbitration_id=0x7e5, is_extended_id=False, dlc=8,
                            data=[0x4c, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0])]
    assert messages[0].equals(expected[0])
    assert messages[1].equals(expected[1])
