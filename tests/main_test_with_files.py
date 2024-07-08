import pytest

from convert_trc_file import trc_line_to_out_line
from utils import assert_lines_are_similar

zipped_lines_from_dcf_out_dcf_trc = [('1      1160.457 FD     0715 Rx 1  7F', '1    1160.5 HB    N:21  PREOPERATIONAL'),
                                     ('2      1209.897 FD     0716 Rx 1  7F', '2    1209.9 HB    N:22  PREOPERATIONAL'),
                                     ('3      3160.412 FD     0715 Rx 1  7F', '3    3160.4 HB    N:21  PREOPERATIONAL'),
                                     ('4      3209.852 FD     0716 Rx 1  7F', '4    3209.9 HB    N:22  PREOPERATIONAL'),
                                     ('5      5160.465 FD     0715 Rx 1  7F', '5    5160.5 HB    N:21  PREOPERATIONAL'),
                                     ('6      5209.905 FD     0716 Rx 1  7F', '6    5209.9 HB    N:22  PREOPERATIONAL'),
                                     ('7      7160.662 FD     0715 Rx 1  7F', '7    7160.7 HB    N:21  PREOPERATIONAL'),
                                     ('8      7210.102 FD     0716 Rx 1  7F', '8    7210.1 HB    N:22  PREOPERATIONAL'),
                                     ('9      9160.659 FD     0715 Rx 1  7F', '9    9160.7 HB    N:21  PREOPERATIONAL'),
                                     ('10      9210.098 FD     0716 Rx 1  7F',
                                      '10    9210.1 HB    N:22  PREOPERATIONAL'),
                                     ('11     11215.898 FD     0751 Rx 1  00', '11   11215.9 HB    N:81 BOOT UP'),
                                     ('12     11160.525 FD     0715 Rx 1  7F',
                                      '12   11160.5 HB    N:21  PREOPERATIONAL'),
                                     ('13     12533.958 FD     007A Rx 0', '13   12534.0 DCL indication'), (
                                         '14     12534.374 FD     0651 Rx 6  15 11 01 00 00 10',
                                         '14   12534.4 USDO  N:81      UlReq 0x1000.0.Device Type'), (
                                         '15     11190.285 FD     0595 Rx 12 51 31 01 00 00 10 05 01 01 CC CC CC',
                                         '15   11190.3 USDO  N:21      UlRsp 0x1000.0.Device Type 1, <0x1>'),
                                     ('16     11209.964 FD     0716 Rx 1  7F',
                                      '16   11210.0 HB    N:22  PREOPERATIONAL'), (
                                         '17     12575.174 FD     0651 Rx 6  15 11 02 00 01 10',
                                         '17   12575.2 USDO  N:81      UlReq 0x1001.0.Error Register'),
                                     ('18     12575.551 FD     007A Rx 0', '18   12575.6 DCL indication'), (
                                         '19     11240.276 FD     0595 Rx 12 51 31 02 00 01 10 05 01 81 CC CC CC',
                                         '19   11240.3 USDO  N:21      UlRsp 0x1001.0.Error Register 129, <0x81>'), (
                                         '20     12623.974 FD     0651 Rx 6  16 11 03 00 00 10',
                                         '20   12624.0 USDO  N:81      UlReq 0x1000.0.Device Type'), (
                                         '21     11279.724 FD     0596 Rx 12 51 31 03 00 00 10 05 01 01 CC CC CC',
                                         '21   11279.7 USDO  N:22      UlRsp 0x1000.0.Device Type 1, <0x1>'), (
                                         '22     12661.998 FD     0651 Rx 6  15 11 04 01 18 10',
                                         '22   12662.0 USDO  N:81      UlReq 0x1018.1.Vendor ID'),
                                     ('23     11320.292 FD     0595 Rx 12 51 31 04 01 18 10 07 04 A4 01 00 00',
                                      '23   11320.3 USDO  N:21      UlRsp 0x1018.1.Vendor ID 420, <0x1a4>'), (
                                         '24     12701.835 FD     0651 Rx 6  16 11 05 00 01 10',
                                         '24   12701.8 USDO  N:81      UlReq 0x1001.0.Error Register'), (
                                         '25     11359.716 FD     0596 Rx 12 51 31 05 00 01 10 05 01 81 CC CC CC',
                                         '25   11359.7 USDO  N:22      UlRsp 0x1001.0.Error Register 129, <0x81>'), (
                                         '26     12742.900 FD     0651 Rx 6  15 11 06 02 18 10',
                                         '26   12742.9 USDO  N:81      UlReq 0x1018.2.Product Code'), (
                                         '27     11400.298 FD     0595 Rx 12 51 31 06 02 18 10 07 04 0B 00 00 00',
                                         '27   11400.3 USDO  N:21      UlRsp 0x1018.2.Product Code 11, <0xb>'), (
                                         '28     12774.220 FD     0651 Rx 6  16 11 07 01 18 10',
                                         '28   12774.2 USDO  N:81      UlReq 0x1018.1.Vendor ID'),
                                     ('29     11439.701 FD     0596 Rx 12 51 31 07 01 18 10 07 04 A4 01 00 00',
                                      '29   11439.7 USDO  N:22      UlRsp 0x1018.1.Vendor ID 420, <0x1a4>'), (
                                         '30     12821.296 FD     0651 Rx 6  15 11 08 03 18 10',
                                         '30   12821.3 USDO  N:81      UlReq 0x1018.3.Revision Number'), (
                                         '31     11480.259 FD     0595 Rx 12 51 31 08 03 18 10 07 04 00 01 01 01',
                                         '31   11480.3 USDO  N:21      UlRsp 0x1018.3.Revision Number 16843008, <0x1010100>'),
                                     (
                                         '32     12861.169 FD     0651 Rx 6  16 11 09 02 18 10',
                                         '32   12861.2 USDO  N:81      UlReq 0x1018.2.Product Code'), (
                                         '33     11519.699 FD     0596 Rx 12 51 31 09 02 18 10 07 04 0B 00 00 00',
                                         '33   11519.7 USDO  N:22      UlRsp 0x1018.2.Product Code 11, <0xb>'), (
                                         '34     12893.676 FD     0651 Rx 6  15 11 0A 04 18 10',
                                         '34   12893.7 USDO  N:81      UlReq 0x1018.4.Serial Number'), (
                                         '35     11550.267 FD     0595 Rx 12 51 31 0A 04 18 10 07 04 3B 00 00 00',
                                         '35   11550.3 USDO  N:21      UlRsp 0x1018.4.Serial Number 59, <0x3b>'), (
                                         '36     12930.315 FD     0651 Rx 6  16 11 0B 03 18 10',
                                         '36   12930.3 USDO  N:81      UlReq 0x1018.3.Revision Number'), (
                                         '37     11589.699 FD     0596 Rx 12 51 31 0B 03 18 10 07 04 00 01 01 01',
                                         '37   11589.7 USDO  N:22      UlRsp 0x1018.3.Revision Number 16843008, <0x1010100>'),
                                     (
                                         '38     12969.851 FD     0651 Rx 6  15 11 0C 00 08 10',
                                         '38   12969.9 USDO  N:81      UlReq 0x1008.0.Manufacturer Device Name'), (
                                         '39     11630.506 FD     0595 Rx 16 51 31 0C 00 08 10 09 06 52 4D 50 38 33 30 CC CC',
                                         '39   11630.5 USDO  N:21      UlRsp 0x1008.0.Manufacturer Device Name RMP830ÌÌ'),
                                     (
                                         '40     13002.154 FD     0651 Rx 6  16 11 0D 04 18 10',
                                         '40   13002.2 USDO  N:81      UlReq 0x1018.4.Serial Number'), (
                                         '41     11659.706 FD     0596 Rx 12 51 31 0D 04 18 10 07 04 2C 00 00 00',
                                         '41   11659.7 USDO  N:22      UlRsp 0x1018.4.Serial Number 44, <0x2c>'), (
                                         '42     13039.313 FD     0651 Rx 6  15 11 0E 00 09 10',
                                         '42   13039.3 USDO  N:81      UlReq 0x1009.0.Manufacturer Hardware Version'), (
                                         '43     11700.482 FD     0595 Rx 16 51 31 0E 00 09 10 09 05 31 2E 30 2E 30 CC CC CC',
                                         '43   11700.5 USDO  N:21      UlRsp 0x1009.0.Manufacturer Hardware Version 1.0.0ÌÌÌ'),
                                     (
                                         '44     13087.162 FD     0651 Rx 6  16 11 0F 00 08 10',
                                         '44   13087.2 USDO  N:81      UlReq 0x1008.0.Manufacturer Device Name'), (
                                         '45     11749.937 FD     0596 Rx 16 51 31 0F 00 08 10 09 06 52 4D 50 38 33 30 CC CC',
                                         '45   11749.9 USDO  N:22      UlRsp 0x1008.0.Manufacturer Device Name RMP830ÌÌ'),
                                     ('46     13127.550 FD     0651 Rx 6  15 11 10 00 00 21',
                                      '46   13127.5 USDO  N:81      UlReq 0x2100.0.'), (
                                         '47     11789.905 FD     0595 Rx 7  51 7F 10 00 00 21 33',
                                         '47   11789.9 USDO  N:21 USDO abort 0x2100.0. Data object does not exist in the object dictionary'),
                                     (
                                         '48     13176.422 FD     0651 Rx 6  16 11 11 00 09 10',
                                         '48   13176.4 USDO  N:81      UlReq 0x1009.0.Manufacturer Hardware Version'), (
                                         '49     11839.921 FD     0596 Rx 16 51 31 11 00 09 10 09 05 31 2E 30 2E 30 CC CC CC',
                                         '49   11839.9 USDO  N:22      UlRsp 0x1009.0.Manufacturer Hardware Version 1.0.0ÌÌÌ'),
                                     (
                                         '50     13229.654 FD     0651 Rx 6  15 11 12 00 0A 10',
                                         '50   13229.7 USDO  N:81      UlReq 0x100a.0.Manufacturer Software Version'), (
                                         '51     11891.064 FD     0595 Rx 24 51 31 12 00 0A 10 09 0F 52 4D 50 38 33 30 20 31 2E 31 2E 30 2E 32 34 CC',
                                         '51   11891.1 USDO  N:21      UlRsp 0x100a.0.Manufacturer Software Version RMP830 1.1.0.24Ì'),
                                     ('52     13279.901 FD     0651 Rx 6  16 11 13 00 00 21',
                                      '52   13279.9 USDO  N:81      UlReq 0x2100.0.'), (
                                         '53     11939.336 FD     0596 Rx 7  51 7F 13 00 00 21 33',
                                         '53   11939.3 USDO  N:22 USDO abort 0x2100.0. Data object does not exist in the object dictionary'),
                                     ('54     13321.213 FD     0651 Rx 6  15 11 14 06 63 1F',
                                      '54   13321.2 USDO  N:81      UlReq 0x1f63.6.'), (
                                         '55     11980.231 FD     0595 Rx 12 51 31 14 06 63 1F 05 01 00 CC CC CC',
                                         '55   11980.2 USDO  N:21      UlRsp 0x1f63.6. 0, <0x0>'), (
                                         '56     13361.691 FD     0651 Rx 6  16 11 15 00 0A 10',
                                         '56   13361.7 USDO  N:81      UlReq 0x100a.0.Manufacturer Software Version'), (
                                         '57     12020.503 FD     0596 Rx 24 51 31 15 00 0A 10 09 0F 52 4D 50 38 33 30 20 31 2E 31 2E 30 2E 32 34 CC',
                                         '57   12020.5 USDO  N:22      UlRsp 0x100a.0.Manufacturer Software Version RMP830 1.1.0.24Ì'),
                                     ('58     13402.134 FD     0651 Rx 6  15 11 16 08 63 1F',
                                      '58   13402.1 USDO  N:81      UlReq 0x1f63.8.'), (
                                         '59     12060.231 FD     0595 Rx 12 51 31 16 08 63 1F 05 01 00 CC CC CC',
                                         '59   12060.2 USDO  N:21      UlRsp 0x1f63.8. 0, <0x0>'),
                                     ('60     13443.050 FD     0651 Rx 6  16 11 17 06 63 1F',
                                      '60   13443.0 USDO  N:81      UlReq 0x1f63.6.'), (
                                         '61     12099.670 FD     0596 Rx 12 51 31 17 06 63 1F 05 01 00 CC CC CC',
                                         '61   12099.7 USDO  N:22      UlRsp 0x1f63.6. 0, <0x0>'), (
                                         '62     13482.242 FD     0651 Rx 6  15 11 18 01 20 10',
                                         '62   13482.2 USDO  N:81      UlReq 0x1020.1.Subindex 1'), (
                                         '63     12140.278 FD     0595 Rx 12 51 31 18 01 20 10 07 04 00 00 00 00',
                                         '63   12140.3 USDO  N:21      UlRsp 0x1020.1.Subindex 1 0, <0x0>'),
                                     ('64     13513.919 FD     0651 Rx 6  16 11 19 08 63 1F',
                                      '64   13513.9 USDO  N:81      UlReq 0x1f63.8.'), (
                                         '65     12169.661 FD     0596 Rx 12 51 31 19 08 63 1F 05 01 00 CC CC CC',
                                         '65   12169.7 USDO  N:22      UlRsp 0x1f63.8. 0, <0x0>'), (
                                         '66     13546.726 FD     0651 Rx 12 15 01 1A 00 17 10 00 02 D0 07 00 00',
                                         '66   13546.7 USDO  N:81   DlExpReq 0x1017.0.Producer Heartbeat Time 2000, <0x7d0>'),
                                     (
                                         '67     12209.821 FD     0595 Rx 6  51 21 1A 00 17 10',
                                         '67   12209.8 USDO  N:21  DlExpResp 0x1017.0.Producer Heartbeat Time'), (
                                         '68     13594.839 FD     0651 Rx 6  16 11 1B 01 20 10',
                                         '68   13594.8 USDO  N:81      UlReq 0x1020.1.Subindex 1'), (
                                         '69     12259.709 FD     0596 Rx 12 51 31 1B 01 20 10 07 04 00 00 00 00',
                                         '69   12259.7 USDO  N:22      UlRsp 0x1020.1.Subindex 1 0, <0x0>'),
                                     ('70     13645.120 FD     0651 Rx 6  15 11 1C 01 34 12',
                                      '70   13645.1 USDO  N:81      UlReq 0x1234.1.'), (
                                         '71     12309.892 FD     0595 Rx 7  51 7F 1C 01 34 12 33',
                                         '71   12309.9 USDO  N:21 USDO abort 0x1234.1. Data object does not exist in the object dictionary'),
                                     ('72     13210.031 FD     0716 Rx 1  7F',
                                      '72   13210.0 HB    N:22  PREOPERATIONAL'),
                                     ('73     14210.682 FD     0715 Rx 1  7F',
                                      '73   14210.7 HB    N:21  PREOPERATIONAL'),
                                     ('74     15210.135 FD     0716 Rx 1  7F',
                                      '74   15210.1 HB    N:22  PREOPERATIONAL')]

from pathlib import Path


def read_and_zip(trc_path):
    with open(trc_path) as trc_file:
        with open(Path(trc_path).with_suffix('.out')) as out_file:
            trc_lines = trc_file.readlines()[11:]
            out_lines = out_file.readlines()
            zipped_list = list(zip([x.strip() for x in trc_lines], [x.strip() for x in out_lines]))
            return zipped_list


@pytest.mark.parametrize(
    "line_from_trc_file,line_from_out_file", read_and_zip('dcf.trc'),
)
def test_dcf(line_from_trc_file, line_from_out_file):
    assert_lines_are_similar(trc_line_to_out_line(line_from_trc_file), line_from_out_file)


"""
@pytest.mark.parametrize(
    "line_from_trc_file,line_from_out_file", read_and_zip('15_05_02.17.trc'),
)
def test_out_file(line_from_trc_file, line_from_out_file):
    assert_lines_are_similar(trc_line_to_out_line(line_from_trc_file), line_from_out_file)

"""
