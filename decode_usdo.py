import can
from enum import IntEnum

from dataclasses import dataclass


def convertLongToAsciiHex(num):
    # Convert long to ASCII string
    # Convert long to hexadecimal string
    return f"{str(num)}, <{hex(num)}>"


@dataclass
class SDOInfo:
    messageType = ""
    operation = ""
    nodeId = 0
    index = 0
    subindex = 0
    dataLength = 0
    data = ""
    datatype = 0
    scs = 0
    value = ""
    hexValue = ""
    description = ""


class DataType(IntEnum):
    BOOLEAN = 0x1
    INTEGER8 = 0x2
    INTEGER16 = 0x3
    INTEGER32 = 0x4
    UNSIGNED8 = 0x5
    UNSIGNED16 = 0x6
    UNSIGNED32 = 0x7
    REAL32 = 0x8
    VISIBLE_STRING = 0x9
    OCTET_STRING = 0xa
    UNICODE_STRING = 0xb
    TIME_OF_DAY = 0xc
    TIME_DIFFERENCE = 0xd
    CANDOMAIN = 0xf
    INTEGER24 = 0x10
    REAL64 = 0x11
    INTEGER40 = 0x12
    INTEGER48 = 0x13
    INTEGER56 = 0x14
    INTEGER64 = 0x15
    UNSIGNED24 = 0x16
    UNSIGNED40 = 0x18
    UNSIGNED48 = 0x19
    UNSIGNED56 = 0x1a
    UNSIGNED64 = 0x1b
    PDO_COMMUNICATION_PARAMETER = 0x20
    PDO_MAPPING_PARAMETER = 0x21
    IDENTITY = 0x23
    OS_DEBUG = 0x24
    OS_COMMAND = 0x25
    ACTIVE_ERROR_HISTORY = 0x26


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

CANopen_dict = {
    0x1000: {0: "Device Type"},
    0x1001: {0: "Error Register"},
    0x1002: {0: "Manufacturer Status Register"},
    0x1003: {0: "Pre-Defined Error Field", 1: "Error Field 1", 2: "Error Field 2"},  # ...
    0x1005: {0: "COB-ID SYNC"},
    0x1006: {0: "Communication Cycle Period"},
    0x1007: {0: "SYNC Window Length"},
    0x1008: {0: "Manufacturer Device Name"},
    0x1009: {0: "Manufacturer Hardware Version"},
    0x100A: {0: "Manufacturer Software Version"},
    0x1010: {0: "Store Parameters", 1: "Store Parameter 1", 2: "Store Parameter 2"},  # ...
    0x1011: {0: "Restore Default Parameters", 1: "Restore Default Parameter 1", 2: "Restore Default Parameter 2"},
    # ...
    0x1012: {0: "COB-ID TIME"},
    0x1013: {0: "High Resolution Timestamp"},
    0x1014: {0: "COB-ID EMCY"},
    0x1015: {0: "Inhibit Time EMCY"},
    0x1016: {0: "Consumer Heartbeat Time", 1: "Consumer Heartbeat Time 1", 2: "Consumer Heartbeat Time 2"},  # ...
    0x1017: {0: "Producer Heartbeat Time"},
    0x1018: {0: "Number of Entries", 1: "Vendor ID", 2: "Product Code", 3: "Revision Number", 4: "Serial Number"},
    0x1019: {0: "Synchronous Counter Overflow Value"},
    0x1020: {0: "Verify Configuration", 1: "Subindex 1", 2: "Subindex 2"},  # ...
    0x1021: {0: "Store EDS", 1: "Subindex 1", 2: "Subindex 2"},  # ...
    0x1022: {0: "Store Format", 1: "Subindex 1", 2: "Subindex 2"},  # ...
    0x1023: {0: "OS Command", 1: "Subindex 1", 2: "Subindex 2"},  # ...
    0x1024: {0: "OS Command Mode", 1: "Subindex 1", 2: "Subindex 2"},  # ...
    0x1025: {0: "OS Debug Mode", 1: "Subindex 1", 2: "Subindex 2"},  # ...
    0x1026: {0: "OS Programming Mode", 1: "Subindex 1", 2: "Subindex 2"},  # ...
    0x1027: {0: "OS Device Description", 1: "Subindex 1", 2: "Subindex 2"},  # ...
    0x1028: {0: "OS Error Behavior", 1: "Subindex 1", 2: "Subindex 2"},  # ...
    0x1029: {0: "Communication Mode", 1: "Subindex 1", 2: "Subindex 2"},  # ...
    0x1200: {0: "SDO Server Parameter", 1: "Subindex 1", 2: "Subindex 2"},  # ...
    0x1280: {0: "SDO Client Parameter", 1: "Subindex 1", 2: "Subindex 2"},  # ...
    0x1400: {0: "Number of Entries", 1: "COB-ID used by RPDO", 2: "Transmission Type"},
    0x1600: {0: "Number of Entries",
             1: "Mapped Object 1",
             2: "Mapped Object 2",
             3: "Mapped Object 3",
             4: "Mapped Object 4",
             5: "Mapped Object 5",
             6: "Mapped Object 6",
             7: "Mapped Object 7",
             8: "Mapped Object 8",
             9: "Mapped Object 9",
             10: "Mapped Object 10",
             11: "Mapped Object 11",
             12: "Mapped Object 12",
             13: "Mapped Object 13",
             14: "Mapped Object 14",
             15: "Mapped Object 15",
             16: "Mapped Object 16",
             17: "Mapped Object 17",
             18: "Mapped Object 18",
             19: "Mapped Object 19",
             20: "Mapped Object 20",
             21: "Mapped Object 21",
             22: "Mapped Object 22",
             23: "Mapped Object 23",
             24: "Mapped Object 24",
             25: "Mapped Object 25",
             26: "Mapped Object 26",
             27: "Mapped Object 27",
             28: "Mapped Object 28",
             29: "Mapped Object 29",
             30: "Mapped Object 30",
             31: "Mapped Object 31",
             32: "Mapped Object 32"},  # ...
    0x1800: {0: "Number of Entries", 1: "COB-ID used by TPDO", 2: "Transmission Type", 3: "Inhibit Time",
             5: "Event Timer", 6: "SYNC Start Value"},
    0x1A00: {0: "Number of Entries",
             1: "Mapped Object 1",
             2: "Mapped Object 2",
             3: "Mapped Object 3",
             4: "Mapped Object 4",
             5: "Mapped Object 5",
             6: "Mapped Object 6",
             7: "Mapped Object 7",
             8: "Mapped Object 8",
             9: "Mapped Object 9",
             10: "Mapped Object 10",
             11: "Mapped Object 11",
             12: "Mapped Object 12",
             13: "Mapped Object 13",
             14: "Mapped Object 14",
             15: "Mapped Object 15",
             16: "Mapped Object 16",
             17: "Mapped Object 17",
             18: "Mapped Object 18",
             19: "Mapped Object 19",
             20: "Mapped Object 20",
             21: "Mapped Object 21",
             22: "Mapped Object 22",
             23: "Mapped Object 23",
             24: "Mapped Object 24",
             25: "Mapped Object 25",
             26: "Mapped Object 26",
             27: "Mapped Object 27",
             28: "Mapped Object 28",
             29: "Mapped Object 29",
             30: "Mapped Object 30",
             31: "Mapped Object 31",
             32: "Mapped Object 32"},  # ...
}


def insertCANopenObjects(CANopen_dict):
    # New CANopen Object Dictionary Indexes, Subindexes and Descriptions
    new_CANopen_objects = {
        0x2501: {1: "SDOLoopType"},
        0x2101: {1: "SDODigFilterTime"},
        0x2102: {1: "SDOAnaFilterTime"},
        0x2426: {1: "SDODeadBand"},
        0x2520: {1: "SDODoPulsePeriod"},
        0x2521: {1: "SDODoPulseOnTime"},
        0x2350: {1: "SDOFaultMode"},
        0x2351: {1: "SDOFaultValue"},
        0x2502: {1: "SDOLoopControl"},
        0x2572: {1: "SDOAutoRecovery"},
        0x2503: {1: "SDOResistance"},
        0x2530: {1: "SDOPWMFrequency"},
        0x2532: {1: "SDODitherFrequency"},
        0x2533: {1: "SDODitherAmplitude"}
    }

    # Extend each object with subindexes from 2 to 32
    for object in new_CANopen_objects.values():
        for i in range(2, 33):
            object[i] = object[1]

    # Insert new CANopen objects into the existing dictionary
    CANopen_dict.update(new_CANopen_objects)


insertCANopenObjects(CANopen_dict)

def CANopen_dict_lookup(sdo):
    try:
        return CANopen_dict[sdo.index][sdo.subindex]
    except KeyError:
        return ""

def parse_canopen_usdo_server_message(msg: can.Message):
    sdo = SDOInfo()
    destination = msg.data[0]
    sdo.scs = msg.data[1]
    sid = msg.data[2]
    is_read = (sdo.scs & 0x60) == 0x40
    is_write = (sdo.scs & 0x60) == 0x20
    sdo.nodeId = msg.arbitration_id & 0x7F

    if sdo.scs == 0x21:
        sdo.index = msg.data[4] + (msg.data[5] << 8)
        sdo.subindex = msg.data[3]
        sdo.operation = getCmdCodeTextUsdo(sdo.scs)
        sdo.messageType = ""
        sdo.description = CANopen_dict_lookup(sdo)

    elif sdo.scs == 0x7f:
        sdo.index = msg.data[4] + (msg.data[5] << 8)
        sdo.subindex = msg.data[3]
        sdo.operation = getCmdCodeTextUsdo(sdo.scs)
        sdo.data = ''.join([f'{i:02x}' for i in msg.data[6:]])
        sdo.value = valueFormat(DataType.UNSIGNED8, 6, msg.data)
        sdo.description = CANopen_dict_lookup(sdo)
        sdo.value = USDO_ERROR_MESSAGES[msg.data[6]]

    elif sdo.scs == 0x31:
        sid = msg.data[2]
        is_read = (sdo.scs & 0x60) == 0x40
        is_write = (sdo.scs & 0x60) == 0x20

        datatype = msg.data[6]
        valueStart = 6

        sdo.index = msg.data[4] + (msg.data[5] << 8)
        sdo.subindex = msg.data[3]
        sdo.dataLength = msg.dlc - 6
        sdo.data = ''.join([f'{i:02x}' for i in msg.data[6:]])

        sdo.operation = getCmdCodeTextUsdo(sdo.scs)
        sdo.messageType = ""
        sdo.value = valueFormat(datatype, 8, msg.data)
        sdo.description = CANopen_dict_lookup(sdo)

    else:
        sdo.nodeId = msg.arbitration_id & 0x7F
        sdo.operation = getCmdCodeTextUsdo(sdo.scs)
        sdo.messageType = ""
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
        sdo.dataLength = msg.dlc - 6
        sdo.nodeId = msg.arbitration_id & 0x7F
        sdo.data = ''.join([f'{i:02x}' for i in msg.data[8:]])

        if sdo.index == 0x1017:
            datatype = DataType.UNSIGNED16
        elif (sdo.index & 0xff00) == 0x1800 and (sdo.subindex == 2):
            datatype = DataType.UNSIGNED8
        elif (sdo.index & 0xff00) in [0x1600, 0x1a00] and (sdo.subindex > 0):
            datatype = DataType.PDO_MAPPING_PARAMETER
        else:
            datatype = msg.data[7]

        sdo.value = valueFormat(datatype, 8, msg.data)
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


def valueFormat(datatype, valueStart, data):
    value = ""

    if datatype == DataType.INTEGER8:
        b = data[valueStart]
        value = convertLongToAsciiHex(b)

    elif datatype == DataType.INTEGER16:
        s = data[valueStart] + (data[valueStart + 1] << 8)
        value = convertLongToAsciiHex(s)

    elif datatype == DataType.INTEGER32:
        l = (data[valueStart] + (data[valueStart + 1] << 8) + (data[valueStart + 2] << 16) + (
                data[valueStart + 3] << 24))
        value = convertLongToAsciiHex(l)

    elif datatype == DataType.UNSIGNED8:
        ub = data[valueStart]
        value = convertLongToAsciiHex(ub)

    elif datatype == DataType.UNSIGNED16:
        us = data[valueStart] + (data[valueStart + 1] << 8)
        value = convertLongToAsciiHex(us)

    elif datatype == DataType.UNSIGNED32:
        l = (data[valueStart] + (data[valueStart + 1] << 8) + (data[valueStart + 2] << 16) + (
                data[valueStart + 3] << 24))
        value = convertLongToAsciiHex(l)

    elif datatype == DataType.VISIBLE_STRING:
        str = ''.join([chr(i) for i in data[valueStart:]])
        value = str

    elif datatype == DataType.PDO_MAPPING_PARAMETER:
        index = data[valueStart + 2] + (data[valueStart + 3] << 8)
        subindex = data[valueStart + 1]
        length = data[valueStart]
        value = f"{index:x}.{subindex}  Length: {length}"

    return value
