import abc
import asyncio
import binascii
import re
import socket
from typing import Optional


RX_PORT = 2001
TX_PORT = 2000
TX_ADDR = "127.0.0.2"
RX_ADDR = "127.0.0.1"


class Phy(abc.ABC):
    """A class that reads & writes bytes to a piece of hardware."""

    @abc.abstractmethod
    async def read(self, max: int) -> [bytes, Exception]:
        """
        Read at most `max` bytes from the underlying hardware.

        Arguments:
            max:
                The maximum number of bytes to read from the underlying interface.
                Unlike the traditional POSIX file interface, a value of -1 will not
                read until "EOF". `max` must be a positive non-zero integer.

        Returns:
            A bytes object of, where `max >= len(result) >= 1`.
        """
        ...

    @abc.abstractmethod
    async def write(self, data: bytes) -> [None, Exception]:
        """
        Write all the specified bytes to the underlying hardware.

        Arguments:
            data: The bytes to write to the hardware.
        """
        await asyncio.sleep(0)


class PhyLy(Phy):
    def __init__(
        self,
        local_addr=("0.0.0.0", 0),
        tx_addr=(TX_ADDR, TX_PORT),
        rx_port=(RX_ADDR, RX_PORT),
    ):
        self.local_addr = local_addr
        self.tx_addr = tx_addr
        self.rx_port = rx_port
        self._tx_sock: Optional[socket.socket] = None
        self._rx_sock: Optional[socket.socket] = None
        self.loop = None

        self.read_queue = asyncio.Queue()
        self.write_queue = asyncio.Queue()

        self._tx_task = None
        self._rx_task = None

    async def initialize(self):
        self.loop = asyncio.get_running_loop()

        self._tx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self._rx_sock.setblocking(False)
        self._tx_sock.setblocking(False)

        print(f"rx_port: {self.rx_port}")
        rx_addr, rx_port = self.rx_port
        self._rx_sock.bind((rx_addr, rx_port))
        print(f"UDP RX on 127.0.0.1:{self.rx_port}")
        tx_ip, tx_port = self.tx_addr
        print(f"UDP TX on {tx_ip}:{tx_port}")

        self._tx_task = asyncio.create_task(self._tx_loop())
        self._rx_task = asyncio.create_task(self._rx_loop())

    async def _tx_loop(self):
        while True:
            data = await self.write_queue.get()

            if data is not None:
                await self.loop.sock_sendto(self._tx_sock, data, self.tx_addr)
                print(f"TX COMPLETED, sent {data}")
                await asyncio.sleep(0.1)

    async def _rx_loop(self):
        while True:
            try:
                data, addr = await asyncio.wait_for(
                    self.loop.sock_recvfrom(self._rx_sock, 65535), timeout=6
                )

                await self.read_queue.put(data)
                hexdump(data)
            except asyncio.TimeoutError:
                print(
                    "#######################################################TIMEOUT ERROR WAITING FOR PING"
                )
                continue
            except Exception as e:
                print(f"Read error: {e}")
                break

    async def write(self, data: bytes) -> [None, Exception]:
        await self.write_queue.put(gen_packet(data))
        print("Successful Write to Queue from Airmac")

    async def read(self):
        data = await self.read_queue.get()
        print(
            "#####################################################Retrieved data from Queue, pumping to Airmac. Recieved:"
        )
        hexdump(data)
        return data


def hexdump(data: bytes) -> None:
    hexstr = binascii.hexlify(data)
    hexstr = b" ".join(hexstr[i : i + 2] for i in range(0, len(hexstr), 2))
    text = re.sub(r"[^a-zA-Z]+".encode(), b".", data)
    print(f"{hexstr} \t {text.decode()}")


def _generate_crc16_table(poly: int) -> list[int]:
    """Generates a 16-bit CRC table for a CRC-CCITT-BR CRC."""
    result = [0] * 256

    # code modified from https://github.com/lammertb/libcrc/blob/master/src/crc16.c#L134
    for i in range(256):
        crc = i << 8

        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc = crc << 1
            crc = crc & 0xFFFF

        result[i] = crc
    return result


CRC16_POLY = 0x1021
CRC16_TABLE = _generate_crc16_table(CRC16_POLY)

# TODO: perhaps we need to use reflected


def crc16(data: bytes, *, init: int = 0xFFFF) -> int:
    """Calculates a 16-bit CRC using the CRC-CCITT-BR polynomial."""
    crc = init
    for value in data:
        byte = (value ^ (crc >> 8)) & 0xFF
        crc = CRC16_TABLE[byte] ^ (crc << 8)
        crc &= 0xFFFF

    # optional: add final XOR value here?
    return crc


def gen_packet(data: str | bytes) -> bytes:
    """Gen packet."""
    if isinstance(data, str):
        data = data.encode()
        frame = bytes([len(data), *data])

    else:
        frame = bytes([len(data), *data])
    print(f"crc 16: {crc16(frame).to_bytes(2, 'big')}")
    hexdump(frame)
    return b"\xaa" * 5 + b"\x7e" + frame + crc16(frame).to_bytes(2, "big")
