import can


def parse_canopen_heartbeat_message(msg: can.Message):
    s = str(msg.arbitration_id & 0x7f)
    data = msg.data[0]
    if data == 0:
        s += " BOOT UP"
    elif data == 4:
        s += " STOPPED"
    elif data == 0x5:
        s += " OPERATIONAL"
    elif data == 127:
        s += " PREOPERATIONAL"
    else:
        s += " ?? NMT STATE"
    return s

# msg = can.Message(timestamp=1453.159, arbitration_id=0x716, is_extended_id=False, dlc=1, data=[0x5], is_fd=True,
#                  bitrate_switch=False, error_state_indicator=False)
