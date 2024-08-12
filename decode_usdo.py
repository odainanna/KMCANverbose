import can

from sdo_utils import CANopen_dict_lookup, DataType, SDOInfo


def convertLongToAsciiHex(num):
    # Convert long to ASCII string
    # Convert long to hexadecimal string
    return f"{str(num)}, <{hex(num)}>"


def getCmdCodeTextUsdo(ccs):
    cmdCodes = {
        0x1: "DlExpReq",
        0x2: "DlSegInitialReq",
        0x3: "Download segmented intermeditate request (segment)",
        0x4: "Download segmented last request (end)",
        0x5: "Reserved for future use by CiA",
        0x6: "Download bulk transfer initial request",
        0x7: "Download bulk transfer segmented",
        0x8: "Download bulk transfer final",
        0x9: "Reserved for future use by CiA",
        0x10: "Reserved for future use by CiA",
        0x11: "UlReq",
        0x12: "Reserved for future use by CiA",
        0x13: "Upload segmented intermediate request (segment)",
        0x14: "Reserved for future use by CiA",
        0x15: "Reserved for future use by CiA",
        0x16: "Reserved for future use by CiA",
        0x17: "Reserved for future use by CiA",
        0x18: "Reserved for future use by CiA",
        0x19: "Reserved for future use by CiA",
        0x20: "Reserved for future use by CiA",
        0x21: "DlExpResp",
        0x22: "Download segmented initial response",
        0x23: "Download segmented intermeditate response (segment)",
        0x24: "Download segmented last response (end)",
        0x25: "Reserved for future use by CiA",
        0x26: "Download bulk transfer initial response",
        0x27: "Reserved for compatibility reasons",
        0x28: "Download bulk transfer final response",
        0x29: "Reserved for future use by CiA",
        0x30: "Reserved for future use by CiA",
        0x31: "UlRsp",
        0x32: "Upload segmented initial response",
        0x33: "Upload segmented intermeditate response (segment)",
        0x34: "Upload segmented last response (end)",
        0x35: "Reserved for future use by CiA",
        0x7f: "USDO abort",
        # ... add the rest of your error codes here ...
    }

    return cmdCodes.get(ccs, "???")


USDO_ERROR_MESSAGES = {
    0x10: "Unknown error",
    0x11: "USDO protocol error detected",
    0x12: "USDO time out error",
    0x13: "Unknown command specifier",
    0x14: "Invalid value in counter byte",
    0x15: "Incorrect data size",
    0x16: "Out of memory",
    0x19: "USDO general routing error",
    0x1A: "USDO destination network",
    0x1B: "USDO dest",
    0x1C: "USDO source network unknown",
    0x1D: "USDO source node unknown",
    0x1E: "Unexpected CAN DLC",
    0x1F: "Unexpected multiplexer",
    0x20: "Data transfer not possible; parallel USDO access to the very same sub-index",
    0x21: "Session-ID wrong or unknown",
    0x31: "Attempt to read a write only data element T",
    0x32: "Attempt to write a read only data element",
    0x33: "Data object does not exist in the object dictionary",
    0x34: "Sub-index does not exist",
    0x35: "Access failed due to a hardware error",
    0x36: "Data type does not match, length of service parameter does not match",
    0x37: "Data type does not match, length of service parameter too high",
    0x38: "Data type does not match, length of service parameter too low",
    0x40: "Invalid value for parameter (download only)",
    0x41: "Value of parameter written too high (download only)",
    0x42: "Value of parameter written too low (download only)",
    0x43: "Maximum value is less than minimum value",
    0x44: "Minimum value is higher than maximum value",
    0x45: "CAN-ID and CAN frame format are of access type read-only",
    0x50: "Data element cannot be mapped to the PDO",
    0x51: "The number and length of the data elements to be mapped would exceed PDO length",
    0x52: "Attempt to map a non mappable data element to a PDO",
    0x53: "Attempt to map a data element of PDO access type RPDO to a TPDO",
    0x54: "Attempt to map a data element of PDO access type TPDO to a RPDO",
    0x55: "Attempt to write to PDO parameters, while PDO is valid",
    0x56: "Attempt to write to PDO mapping parameters, while PDO mapping is valid",
    0x60: "Data cannot be transferred or stored to the application",
    0x61: "Data cannot be transferred or stored to the application because of local control",
    0x62: "Data cannot be transferred or stored to the application because of the present device state",
    0x63: "Object dictionary dynamic generation fails or no object dictionary is present",
    0x64: "No data available"
}


def parse_canopen_usdo_server_message(msg: can.Message):
    sdo = SDOInfo()
    destination = msg.data[0]
    sdo.scs = msg.data[1]
    sid = msg.data[2]
    is_read = (sdo.scs & 0x60) == 0x40
    is_write = (sdo.scs & 0x60) == 0x20
    sdo.nodeId = msg.arbitration_id & 0x7F
    sdo.index = msg.data[4] + (msg.data[5] << 8)
    sdo.subindex = msg.data[3]

    if sdo.scs == 0x21:
        # Download expedited response
        sdo.operation = getCmdCodeTextUsdo(sdo.scs)
        sdo.description = CANopen_dict_lookup(sdo)

    elif sdo.scs == 0x7f:
        # USDO abort service
        sdo.operation = getCmdCodeTextUsdo(sdo.scs)
        sdo.data = ''.join([f'{i:02x}' for i in msg.data[6:]])
        # sdo.value, sdo.hexValue = get_value(DataType.UNSIGNED8, 6, msg.data)
        sdo.description = CANopen_dict_lookup(sdo)
        sdo.value = USDO_ERROR_MESSAGES[msg.data[6]]

    elif sdo.scs == 0x31:
        # Upload expedited response
        sid = msg.data[2]
        is_read = (sdo.scs & 0x60) == 0x40
        is_write = (sdo.scs & 0x60) == 0x20
        datatype = msg.data[6]
        valueStart = 6
        sdo.dataLength = msg.data[7]
        sdo.data = ''.join([f'{i:02x}' for i in msg.data[6:6+sdo.dataLength]])
        sdo.operation = getCmdCodeTextUsdo(sdo.scs)
        sdo.value, sdo.hexValue = get_value(datatype, 8, msg.data[:8+sdo.dataLength])
        sdo.description = CANopen_dict_lookup(sdo)
    else:
        sdo.nodeId = msg.arbitration_id & 0x7F
        sdo.operation = getCmdCodeTextUsdo(sdo.scs)
        sdo.value = ""
    return sdo


def parse_canopen_usdo_client_message(msg: can.Message):
    sdo = SDOInfo()
    destination = msg.data[0]
    sdo.scs = msg.data[1]

    if sdo.scs == 0x1:
        sdo.operation = getCmdCodeTextUsdo(sdo.scs)
        sdo.index = msg.data[4] + (msg.data[5] << 8)
        sdo.subindex = msg.data[3]
        sdo.dataLength = msg.data[7]
        sdo.nodeId = msg.arbitration_id & 0x7F
        data = msg.data[8:8+sdo.dataLength]

        sdo.data = ''.join([f'{i:02x}' for i in data])

        if sdo.index == 0x1017:
            datatype = DataType.UNSIGNED16
        elif (sdo.index & 0xff00) == 0x1800 and (sdo.subindex == 2):
            datatype = DataType.UNSIGNED8
        elif (sdo.index & 0xff00) in [0x1600, 0x1a00] and (sdo.subindex > 0):
            datatype = DataType.PDO_MAPPING_PARAMETER
        elif msg.data[6] != 0:
            datatype = msg.data[6]
        elif sdo.dataLength == 1:
            datatype = DataType.UNSIGNED8
        elif sdo.dataLength == 2:
            datatype = DataType.UNSIGNED16
        elif sdo.dataLength == 4:
            datatype = DataType.UNSIGNED32
        else:
            # unknown data type
            datatype = DataType.UNSIGNED32

        sdo.value, sdo.hexValue = get_value(datatype, 8, msg.data[:8+sdo.dataLength])
        sdo.description = CANopen_dict_lookup(sdo)

    elif sdo.scs == 0x11:
        sdo.index = msg.data[4] + (msg.data[5] << 8)
        sdo.subindex = msg.data[3]
        sdo.nodeId = msg.arbitration_id & 0x7F
        sdo.operation = getCmdCodeTextUsdo(sdo.scs)
        sdo.messageType = ""
        sdo.value = ""
        sdo.description = CANopen_dict_lookup(sdo)

    elif sdo.scs in [0x16, 0x31, 0x51]:
        sdo.operation = getCmdCodeTextUsdo(sdo.scs)

    else:
        sdo.operation = getCmdCodeTextUsdo(sdo.scs)
    return sdo


def get_value(datatype, valueStart, data):
    if datatype == DataType.INTEGER8:
        b = data[valueStart]
        return str(b), hex(b)

    elif datatype == DataType.INTEGER16:
        s = data[valueStart] + (data[valueStart + 1] << 8)
        return str(s), hex(s)

    elif datatype == DataType.INTEGER32:
        l = (data[valueStart] + (data[valueStart + 1] << 8) + (data[valueStart + 2] << 16) + (
                data[valueStart + 3] << 24))
        return str(l), hex(l)

    elif datatype == DataType.UNSIGNED8:
        ub = data[valueStart]
        return str(ub), hex(ub)

    elif datatype == DataType.UNSIGNED16:
        us = data[valueStart] + (data[valueStart + 1] << 8)
        return str(us), hex(us)

    elif datatype == DataType.UNSIGNED32:
        l = (data[valueStart] + (data[valueStart + 1] << 8) + (data[valueStart + 2] << 16) + (
                data[valueStart + 3] << 24))
        return str(l), hex(l)

    elif datatype == DataType.VISIBLE_STRING:
        s = ''.join([chr(i) for i in data[valueStart:]])
        return s, ''

    elif datatype == DataType.PDO_MAPPING_PARAMETER:
        index = data[valueStart + 2] + (data[valueStart + 3] << 8)
        subindex = data[valueStart + 1]
        length = data[valueStart]
        value = f"{index:x}.{subindex}  Length: {length}"
        return value, ''

    else:
        return 'unknown datatype'
