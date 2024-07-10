import can

from decode_emcy import parse_canopen_emcy_message
from decode_lss import CANopenLSSCommands
from decode_nmt import parse_canopen_nmt_message
from decode_sdo import parse_canopen_sdo_server_message, parse_canopen_sdo_client_message
from decode_usdo import parse_canopen_usdo_server_message, parse_canopen_usdo_client_message
from hb import parse_canopen_heartbeat_message


def explain_msg(msg):
    def undefined_message_id():
        return "?msg_id: " + str(msg)

    def msg_to_string(msg: can.Message):
        return ""  # str(msg)

    def format_raw_data():
        return f'{msg.arbitration_id:02x} <{' '.join(f"{x:02x}" for x in msg.data)}>'

    def format_sdo(sdo):
        return f'{format_raw_data()} {object.messageType} N:{object.nodeId} {str(object.operation).rjust(10)} {hex(object.index)}.{object.subindex}.{object.description} {object.value} {object.hexValue}'

    def f(cob_type):
        return f'{cob_type} {msg.arbitration_id:02x} <{' '.join(f"{x:02x}" for x in msg.data)}>'

    msg_id = msg.arbitration_id
    try:
        if msg_id == -1:
            return "ERROR"
        elif msg_id == 0:
            return "NMT : " + parse_canopen_nmt_message(msg)
        elif msg_id == 0x7A:
            return "DCL indication"
        elif msg_id == 0x7B:
            return "RCL indication"
        elif msg_id < 0x80:
            return "?msg_id  : " + msg_to_string(msg)
        elif msg_id == 0x80:
            return "SYNC:"
        elif msg_id < 0x100:
            return parse_canopen_emcy_message(msg)
        elif msg_id == 0x100:
            return "TIME " + hex(msg_id) + msg_to_string(msg)
        elif msg_id <= 0x580:
            return "PDO : " + msg_to_string(msg)
        elif msg_id < 0x600:
            if msg.is_fd:
                object = parse_canopen_usdo_server_message(msg)
                return f"USDO {format_sdo(object)}"
            else:
                object = parse_canopen_sdo_server_message(msg)
                return f"SDO {format_sdo(object)}"
        elif msg_id == 0x600:
            return undefined_message_id()
        elif msg_id < 0x680:
            if msg.is_fd:
                object = parse_canopen_usdo_client_message(msg)
                return f"USDO {format_sdo(object)}"
            else:
                object = parse_canopen_sdo_client_message(msg)
                return f"SDO {format_sdo(object)}"
        elif msg_id < 0x700:
            return "PDO : " + msg_to_string(msg)
        elif msg_id == 0x700:
            return undefined_message_id()
        elif msg_id < 0x780:
            return "HB    N:" + parse_canopen_heartbeat_message(msg)
        elif msg_id == 0x7E5:
            if msg.data[0] in CANopenLSSCommands:
                return f"LSS {CANopenLSSCommands[msg.data[0]]}"
            else:
                return "LSS " + msg_to_string(msg)
        else:
            return "QQ" + msg_to_string(msg)  # Add "QQ" and the line to the output string
    except KeyError:
        return ""
