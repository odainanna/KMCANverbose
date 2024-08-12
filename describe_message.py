from decode_emcy import parse_canopen_emcy_message
from decode_lss import CANopenLSSCommands
from decode_nmt import parse_canopen_nmt_message
from decode_sdo import parse_canopen_sdo_server_message, parse_canopen_sdo_client_message
from decode_usdo import parse_canopen_usdo_server_message, parse_canopen_usdo_client_message
from hb import parse_canopen_heartbeat_message


def describe_message(msg):
    def undefined_message_id():
        return "?"

    def format_sdo(sdo):
        s = f'{sdo.messageType} N:{sdo.nodeId} {str(sdo.operation)}'
        if sdo.operation != '?':
            s += f' {hex(sdo.index)}.{sdo.subindex} {sdo.description} {sdo.value} {sdo.hexValue}'
        return s

    msg_id = msg.arbitration_id
    # TODO: see Table 50 – Pre-defined connection set
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
            return undefined_message_id()
        elif msg_id == 0x80:
            return "SYNC:"
        elif msg_id < 0x100:
            return parse_canopen_emcy_message(msg)
        elif msg_id == 0x100:
            return "TIME " + hex(msg_id)
        elif msg_id <= 0x580:
            return "PDO : "
        elif msg_id < 0x600:
            if msg.is_fd:
                return f"USDO {format_sdo(parse_canopen_usdo_server_message(msg))}"
            else:
                return f"SDO {format_sdo(parse_canopen_sdo_server_message(msg))}"
        elif msg_id == 0x600:
            return undefined_message_id()
        elif msg_id < 0x680:
            if msg.is_fd:
                return f"USDO {format_sdo(parse_canopen_usdo_client_message(msg))}"
            else:
                return f"SDO {format_sdo(parse_canopen_sdo_client_message(msg))}"
        elif msg_id < 0x700:
            return "PDO : "
        elif msg_id == 0x700:
            return undefined_message_id()
        elif msg_id < 0x780:
            return "HB    N:" + parse_canopen_heartbeat_message(msg)
        elif msg_id == 0x7E5:
            if msg.data[0] in CANopenLSSCommands:
                return f"LSS {CANopenLSSCommands[msg.data[0]]}"
            else:
                return "LSS"
        else:
            return "QQ"
    except KeyError:
        return ""
