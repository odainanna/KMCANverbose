from enum import Enum


class LSSCommand(Enum):
    SWITCH_STATE_GLOBAL = 0x04
    SWITCH_STATE_SELECTIVE_VENDOR = 0x44
    SWITCH_STATE_SELECTIVE_PRODUCT = 0x45
    SWITCH_STATE_SELECTIVE_REVISION = 0x46
    SWITCH_STATE_SELECTIVE_SERIAL = 0x47
    IDENTIFY_REMOTE_SLAVE = 0x4C
    CONFIGURE_BIT_TIMING = 0x05
    CONFIGURE_NODE_ID = 0x11
    STORE_CONFIGURATION = 0x17
    INQUIRE_IDENTITY_VENDOR = 0x5A
    INQUIRE_IDENTITY_PRODUCT = 0x5B
    INQUIRE_IDENTITY_REVISION = 0x5C
    INQUIRE_IDENTITY_SERIAL = 0x5D
    INQUIRE_NODE_ID = 0x5E


CANopenLSSCommands = {
    int(LSSCommand.SWITCH_STATE_GLOBAL.value): "Switch State Global",
    int(LSSCommand.SWITCH_STATE_SELECTIVE_VENDOR.value): "Switch State Selective Vendor ID",
    int(LSSCommand.SWITCH_STATE_SELECTIVE_PRODUCT.value): "Switch State Selective Product Code",
    int(LSSCommand.SWITCH_STATE_SELECTIVE_REVISION.value): "Switch State Selective Revision Number",
    int(LSSCommand.SWITCH_STATE_SELECTIVE_SERIAL.value): "Switch State Selective Serial Number",
    int(LSSCommand.CONFIGURE_BIT_TIMING.value): "Configure Bit Timing Parameters",
    int(LSSCommand.CONFIGURE_NODE_ID.value): "Configure Node ID",
    int(LSSCommand.STORE_CONFIGURATION.value): "Store Configuration",
    int(LSSCommand.INQUIRE_IDENTITY_VENDOR.value): "Inquire Identity Vendor ID",
    int(LSSCommand.INQUIRE_IDENTITY_PRODUCT.value): "Inquire Identity Product Code",
    int(LSSCommand.INQUIRE_IDENTITY_REVISION.value): "Inquire Identity Revision Number",
    int(LSSCommand.INQUIRE_IDENTITY_SERIAL.value): "Inquire Identity Serial Number",
    int(LSSCommand.INQUIRE_NODE_ID.value): "Inquire Node ID",
    int(LSSCommand.IDENTIFY_REMOTE_SLAVE.value): "Identify remote slave"
}
