from dataclasses import dataclass
from enum import IntEnum


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
