import pytest
from can import Message

from decode_nmt import parse_canopen_nmt_message
from describe_message import describe_message  # replace with actual module name


def test_nmt():
    # Test for NMT message
    msg = Message(timestamp=12956.035, arbitration_id=0x0, dlc=2, data=[0x81, 0x16], is_fd=True)
    assert describe_message(msg) == "NMT : " + parse_canopen_nmt_message(msg)


def test_dcl():
    # Test for DCL indication
    msg = Message(arbitration_id=0x7A, is_fd=False)
    assert describe_message(msg) == "DCL indication"


def test_rcl():
    # Test for RCL indication
    msg = Message(arbitration_id=0x7B, is_fd=False)
    assert describe_message(msg) == "RCL indication"


def test_sync():
    # Test for SYNC
    msg = Message(arbitration_id=0x80, is_fd=False)
    assert describe_message(msg) == "SYNC:"


def test_time():
    # Test for TIME
    msg = Message(arbitration_id=0x100, is_fd=False)
    assert describe_message(msg) == "TIME 0x100"


def test_lss():
    # Test for LSS
    msg = Message(arbitration_id=0x7E5, data=[0x01], is_fd=False)  # assuming 0x01 is a valid LSS command
    assert describe_message(msg) == "LSS"


def test_undefined():
    # Test for undefined message id
    msg = Message(arbitration_id=0x600, is_fd=False)
    assert describe_message(msg) == "?"  # replace with expected output


def test_error():
    # Test for error
    msg = Message(arbitration_id=-1, is_fd=False)
    assert describe_message(msg) == "ERROR"
