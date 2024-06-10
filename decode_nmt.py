import can

# CANopen NMT Commands
NMT_START_REMOTE_NODE = 0x01
NMT_STOP_REMOTE_NODE = 0x02
NMT_ENTER_PRE_OPERATIONAL = 0x80
NMT_RESET_NODE = 0x81
NMT_RESET_COMMUNICATION = 0x82


def parse_canopen_nmt_message(msg: can.Message):
    ret = str(msg.data[1])

    if msg.data[0] == NMT_START_REMOTE_NODE:
        ret += " NMT_START_REMOTE_NODE"
    elif msg.data[0] == NMT_STOP_REMOTE_NODE:
        ret += " NMT_STOP_REMOTE_NODE"
    elif msg.data[0] == NMT_ENTER_PRE_OPERATIONAL:
        ret += " NMT_ENTER_PRE_OPERATIONAL"
    elif msg.data[0] == NMT_RESET_NODE:
        ret += " NMT_RESET_NODE"
    elif msg.data[0] == NMT_RESET_COMMUNICATION:
        ret += " NMT_RESET_COMMUNICATION"
    else:
        ret += "?? NMT STATE"

    return ret
