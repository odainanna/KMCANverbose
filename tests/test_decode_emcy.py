import pytest
from can import Message
from decode_emcy import parse_canopen_emcy_message


def test_parse_canopen_emcy_message_no_error():
    msg = Message(arbitration_id=0x80, data=[0x00, 0x00, 0x00, 0x00])
    assert parse_canopen_emcy_message(msg) == "EMCY N:0 0 Error reset or no error"


def test_parse_canopen_emcy_message_unknown_error():
    msg = Message(arbitration_id=0x80, data=[0xFF, 0xFF, 0x00, 0x00])
    assert parse_canopen_emcy_message(msg) == "EMCY"
