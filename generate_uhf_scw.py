import enum
import serial
import zlib


class RFMode(enum.IntEnum):
    BPS_1200_MODULATION_INDEX_1_0 = 0b000
    BPS_2400_MODULATION_INDEX_0_5 = 0b001
    BPS_4800_MODULATION_INDEX_0_5 = 0b010
    # This is the default for the UHF
    BPS_9600_MODULATION_INDEX_0_5 = 0b011
    BPS_9600_MODULATION_INDEX_1_0 = 0b100
    BPS_19200_MODULATION_INDEX_0_5 = 0b101
    BPS_19200_MODULATION_INDEX_1_0 = 0b110
    BPS_19200_MODULATION_INDEX_2_0 = 0b111


class UartBaud(enum.IntEnum):
    # fmt: off
    UART_9600     = 0b00
    UART_RESERVED = 0b01
    UART_19200    = 0b10
    UART_115200   = 0b11
    # fmt: on


def create_uhf_scw(
    *,
    pipe: bool,
    beacon: bool,
    bootloader: bool = False,
    echo_esttc: bool = False,
    rf_mode: RFMode = RFMode.BPS_9600_MODULATION_INDEX_0_5,
    reset: bool = False,
    uart_baud: UartBaud = UartBaud.UART_115200,
):
    return (
        0b11
        | (int(bootloader) << 4)
        | (int(pipe) << 5)
        | (int(beacon) << 6)
        | (int(echo_esttc) << 7)
        | (int(rf_mode) << 8)
        | (int(reset) << 11)
        | (int(uart_baud) << 12)
    )

def packet_for_cmd(cmd: str) -> bytes:
    crc = zlib.crc32(cmd.encode('ascii'))
    return "{} {:08X}\r".format(cmd, crc).encode()


scw = create_uhf_scw(pipe=True, beacon=True)

port = serial.Serial("/dev/ttyACM0", 115200)
# pkt = packet_for_cmd('ES+R22F9')
pkt = b"\"ES+R22FB 7AE6407F\""
port.write(pkt)
while True:
    line = port.read()
    print(line)
