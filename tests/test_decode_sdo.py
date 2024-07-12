import pytest
from can import Message
from decode_sdo import parse_canopen_sdo_server_message, parse_canopen_sdo_client_message
from sdo_utils import CANopen_dict_lookup


def test_parse_canopen_sdo_server_message():
    msg = Message(arbitration_id=0x600, data=[0x40, 0x00, 0x10, 0x01, 0x00, 0x00, 0x00, 0x00])
    sdo = parse_canopen_sdo_server_message(msg)
    assert sdo.nodeId == 0x00
    assert sdo.index == 0x1000
    assert sdo.subindex == 0x01
    assert sdo.scs == 0x40
    assert sdo.operation == "Exp. Read Req"
    assert sdo.length == 4
    assert sdo.data == bytearray([0x40, 0x00, 0x10, 0x01])
    assert sdo.value == "0"
    assert sdo.hexValue == "0x0"
    assert sdo.description == CANopen_dict_lookup(sdo)


def test_parse_canopen_sdo_client_message():
    msg = Message(arbitration_id=0x580, data=[0x60, 0x00, 0x10, 0x01, 0x00, 0x00, 0x00, 0x00])
    sdo = parse_canopen_sdo_client_message(msg)
    assert sdo.nodeId == 0x00
    assert sdo.index == 0x1000
    assert sdo.subindex == 0x01
    assert sdo.scs == 0x60
    assert sdo.operation == "Write Resp Successful"
    assert sdo.length == 4
    assert sdo.data == bytearray([0x60, 0x00, 0x10, 0x01])
    assert sdo.value == "0"
    assert sdo.hexValue == "0x0"
    assert sdo.description == CANopen_dict_lookup(sdo)
