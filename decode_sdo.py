import can

from sdo_utils import SDOInfo, CANopen_dict_lookup

cmdCodes = {
    0x40: "Exp. Read Req",
    0x41: "Read",
    0x4F: "Exp. Read Req/Resp 1 byte",
    0x4B: "Exp. Read Req/Resp 2 bytes",
    0x43: "Exp. Read Req/Resp 4 bytes",
    0x2F: "Exp. Write Req 1 byte",
    0x2B: "Exp. Write Req 2 bytes",
    0x23: "Exp. Write Req 4 bytes",
    0x60: "Write Resp Successful",
    0x80: "Write Resp Unsuccessful",
}


def parse_canopen_sdo_server_message(msg: can.Message):
    sdo = SDOInfo()

    # Extract the node ID from the COB-ID
    sdo.nodeId = msg.arbitration_id & 0x7f

    # Extract the index and subindex from the data
    data = msg.data

    sdo.index = msg.data[1] + (msg.data[2] << 8)
    sdo.subindex = msg.data[3]

    # Determine if the SDO is a read or write
    sdo.scs = data[0]
    sdo.operation = cmdCodes.get(sdo.scs, '?')

    # Determine the length of the payload
    sdo.length = 4 - ((sdo.scs >> 2) & 0b11)

    # Extract the SDO data
    sdo.data = data[0:sdo.length]

    value = msg.data[4] + (msg.data[5] << 8) + (msg.data[6] << 16) + (msg.data[7] << 24)
    sdo.value = str(value)

    sdo.hexValue = hex(value)
    sdo.description = CANopen_dict_lookup(sdo)

    return sdo


def parse_canopen_sdo_client_message(msg: can.Message):
    return parse_canopen_sdo_server_message(msg)
