import pytest
from can import Message
from decode_nmt import parse_canopen_nmt_message


def test_nmt_start_remote_node():
    msg = Message(data=[0x01, 0x00])
    assert parse_canopen_nmt_message(msg) == "0 NMT_START_REMOTE_NODE"


def test_nmt_stop_remote_node():
    msg = Message(data=[0x02, 0x00])
    assert parse_canopen_nmt_message(msg) == "0 NMT_STOP_REMOTE_NODE"


def test_nmt_enter_pre_operational():
    msg = Message(data=[0x80, 0x00])
    assert parse_canopen_nmt_message(msg) == "0 NMT_ENTER_PRE_OPERATIONAL"


def test_nmt_reset_node():
    msg = Message(data=[0x81, 0x00])
    assert parse_canopen_nmt_message(msg) == "0 NMT_RESET_NODE"


def test_nmt_reset_communication():
    msg = Message(data=[0x82, 0x00])
    assert parse_canopen_nmt_message(msg) == "0 NMT_RESET_COMMUNICATION"


def test_undefined_nmt_state():
    msg = Message(data=[0xFF, 0x00])
    assert parse_canopen_nmt_message(msg) == "0 ?? NMT STATE"
