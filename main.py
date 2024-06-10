import glob
import sys
from pathlib import Path

import can

from decode_emcy import parse_canopen_emcy_message
from decode_lss import CANopenLSSCommands
from decode_nmt import parse_canopen_nmt_message
from decode_usdo import parse_canopen_usdo_client_message, parse_canopen_usdo_server_message, SDOInfo
from hb import parse_canopen_heartbeat_message


def parse_trc_string(line):
    """
    :param line: str like "      1      1453.159 FD     0716 Rx 1  05 "
    :return: line_nr, the line converted to a can.Message object
    """
    parts = line.split()
    try:
        line_nr = int(parts[0])
        timestamp = float(parts[1])
        is_fd = parts[2] == 'FD'
        is_dt = parts[2] == 'DT'
        is_st = parts[2] == 'ST'
        if is_fd or is_dt:
            arbitration_msg_id = int(parts[3], 16)  # Convert hex to int
            is_rx = parts[4] == 'Rx'
            dlc = int(parts[5])
            data = [int(x, 16) for x in parts[6:]]  # Convert hex to int and put in a list
        elif is_st:
            arbitration_msg_id = -1  # the id slot is missing
            is_rx = parts[3] == 'Rx'
            dlc = int(parts[4])
            data = [int(x, 16) for x in parts[5:]]  # Convert hex to int and put in a list
        else:
            raise ValueError(f'Failed to parse {line}')
        return line_nr, can.Message(timestamp=timestamp, is_fd=is_fd, arbitration_id=arbitration_msg_id,
                                    is_rx=is_rx, dlc=dlc, data=data, is_extended_id=False)
    except IndexError:
        raise ValueError(f'Failed to parse {line}')


def generate_explanation(line_nr, msg):
    def undefined_message_id():
        return "?msg_id: " + str(msg)

    def msg_to_string(msg: can.Message):
        return ""  # str(msg)

    output = f"{line_nr} {msg.timestamp:.1f} "
    msg_id = msg.arbitration_id
    try:
        if msg_id == 0:
            output += "NMT : " + parse_canopen_nmt_message(msg)
        elif msg_id == 0x7A:
            output += "DCL indication"
        elif msg_id == 0x7B:
            output += "RCL indication"
        elif msg_id < 0x80:
            output += "?msg_id  : " + msg_to_string(msg)
        elif msg_id == 0x80:
            output += "SYNC:"
        elif msg_id < 0x100:
            output += parse_canopen_emcy_message(msg)
        elif msg_id == 0x100:
            output += "TIME " + hex(msg_id) + msg_to_string(msg)
        elif msg_id <= 0x580:
            output += "PDO : " + msg_to_string(msg)
        elif msg_id < 0x600:
            object = parse_canopen_usdo_server_message(msg)
            output += (f"USDO {object.messageType} N:{object.nodeId} {str(object.operation).rjust(10)} "
                       f"{hex(object.index)}.{object.subindex}.{object.description} {object.value}")
        elif msg_id == 0x600:
            output += undefined_message_id()
        elif msg_id < 0x680:
            object = parse_canopen_usdo_client_message(msg)
            output += (f"USDO {object.messageType} N:{object.nodeId} {str(object.operation).rjust(10)} "
                       f"{hex(object.index)}.{object.subindex}.{object.description} {object.value}")
        elif msg_id == 0x700:
            output += undefined_message_id()
        elif msg_id < 0x780:
            output += "HB    N:" + parse_canopen_heartbeat_message(msg)
        elif msg_id == 0x7E5:
            if msg.data[0] in CANopenLSSCommands:
                output += f"LSS {CANopenLSSCommands[msg.data[0]]}"
            else:
                output += "LSS " + msg_to_string(msg)
        else:
            output += "QQ" + msg_to_string(msg)  # Add "QQ" and the line to the output string
        return output + '\n'
    except KeyError:
        return output + '\n'


def trc_line_to_out_line(line_from_trc_file):
    line_nr, msg = parse_trc_string(line_from_trc_file)
    line_for_output_file = generate_explanation(line_nr, msg)
    return line_for_output_file


def convert_trc_file_to_out_file(path):
    path = Path(path)
    if not path.exists():
        raise ValueError(f'{path} does not exist')
    elif not (path.is_file() and path.suffix == '.trc'):
        raise ValueError(f'{path} should be a .trc-file')
    with (open(path) as trc_file):
        out_path = Path(path).with_suffix('.txt')
        with open(out_path, mode='w') as out_file:
            for line_in in trc_file.readlines():
                if line_in.strip() == "" or line_in.startswith(';'):
                    # skip the header and empty lines in the .trc file
                    continue
                try:
                    line_out = trc_line_to_out_line(line_in)
                except Exception as e:
                    line_out = f'ERROR: {e}'
                out_file.write(line_out)
    return out_path


def main():
    args = sys.argv[1:]
    if not args:
        print('No args. Args should be a list of paths to .trc-files')
    paths = [Path(arg) for arg in args]
    # if paths is a list of files that exist and end with .trc
    if all([path.exists() and path.is_file() for path in paths]):
        trc_files = paths
        for trc_file in trc_files:
            output_file = convert_trc_file_to_out_file(trc_file)
            print(f'Read from {trc_file} and wrote to {output_file}.')
    else:
        raise ValueError('Invalid args. Args should be a list of paths to .trc-files that exist')


if __name__ == '__main__':
    main()
