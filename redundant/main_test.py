from redundant.convert_trc_file import parse_trc_line, trc_line_to_out_line
from utils import assert_lines_are_similar


def check_single_line(line_from_trc_file, line_from_out_file):
    assert_lines_are_similar(trc_line_to_out_line(line_from_trc_file), line_from_out_file)


def test_nmt_0000():
    line_from_trc_file = "      15     12956.035 FD     0000 Rx 2  81 16 "
    line_from_out_file = "15   12956.0 NMT : 22  NMT_RESET_NODE"
    check_single_line(line_from_trc_file, line_from_out_file)


def test_nmt_0x7A():
    line_from_trc_file = "     13     12533.958 FD     007A Rx 0"
    line_from_out_file = "13   12534.0 DCL indication"
    check_single_line(line_from_trc_file, line_from_out_file)


def test_pcan_to_can_message_len_0():
    line_from_trc_file = "      1      1453.159 FD     0716 Rx 0"
    line_nr, msg = parse_trc_line(line_from_trc_file)
    assert line_nr == 1
    assert msg.timestamp == 1453.159
    assert msg.is_fd is True
    assert msg.arbitration_id == 0x0716
    assert msg.is_rx is True
    assert msg.dlc == 0
    assert msg.data == bytearray(b'')


def test_pcan_to_can_message_len_1():
    line_from_trc_file = "      1      1453.159 FD     0716 Rx 1  05 "
    line_nr, msg = parse_trc_line(line_from_trc_file)
    assert msg.timestamp == 1453.159
    assert msg.is_fd is True
    assert msg.arbitration_id == 0x0716
    assert msg.is_rx is True
    assert msg.dlc == 1
    assert msg.data == bytearray(b'\x05')


def test_pcan_to_can_message_len_2():
    line_from_trc_file = "      1      1453.159 FD     0716 Rx 2  05 01"
    line_nr, msg = parse_trc_line(line_from_trc_file)
    assert line_nr == 1
    assert msg.timestamp == 1453.159
    assert msg.is_fd is True
    assert msg.arbitration_id == 0x0716
    assert msg.is_rx is True
    assert msg.dlc == 2
    assert msg.data == bytearray(b'\x05\x01')


def test_heartbeat():
    line_from_trc_file = "      1      1453.159 FD     0716 Rx 1  05 "
    line_from_out_file = "1    1453.2 HB    N:22  OPERATIONAL"
    check_single_line(line_from_trc_file, line_from_out_file)


def test_emcy():
    line_from_trc_file = "     11     11215.898 FD     0751 Rx 1  00"
    line_from_out_file = "11   11215.9 HB    N:81 BOOT UP"
    check_single_line(line_from_trc_file, line_from_out_file)


def test_dcl_indication():
    line_from_trc_file = "     18     12575.551 FD     007A Rx 0"
    line_from_out_file = "18   12575.6 DCL indication"
    check_single_line(line_from_trc_file, line_from_out_file)


def test_usdo():
    line_from_trc_file = "19     11240.276 FD     0595 Rx 12 51 31 02 00 01 10 05 01 81 CC CC CC"
    line_from_out_file = "19   11240.3 USDO  N:21      UlRsp 0x1001.0 Error Register 129, <0x81>"
    check_single_line(line_from_trc_file, line_from_out_file)


def test_emcy():
    line_from_trc_file = "99     11240.276 FD     0095 Rx 08 30 10 00 00 00 00 00 00"
    line_from_out_file = "99   11240.3 EMCY  N:21      1030 Termination Board not supported"
    check_single_line(line_from_trc_file, line_from_out_file)


def test_0595():
    # encoding?
    line_from_trc_file = "     43     11700.482 FD     0595 Rx 16 51 31 0E 00 09 10 09 05 31 2E 30 2E 30 CC CC CC "
    line_from_out_file = "43   11700.5 USDO  N:21      UlRsp 0x1009.0 Manufacturer Hardware Version 1.0.0ÌÌÌ"
    check_single_line(line_from_trc_file, line_from_out_file)
