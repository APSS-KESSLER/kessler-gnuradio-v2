import argparse
import binascii
import re
import asyncio
import socket
from typing import Optional
import zmq
import zmq.asyncio as zmqasync
import pmt
import numpy as np
import time


# From ES UHF II USER MANUAL 2023
UHF_PRE_PAYLOAD = 7  # Preamble + Sync + Payload Length
UHF_POST_PAYLOAD = -2  # CRC

RX_PORT = 2001
TX_PORT = 2000
TX_ADDR = "127.0.0.2"
RX_ADDR = "127.0.0.1"

AIRMAC_PROTOCOL_ID = b"\x01"
RADIO_MODULE_ADDRESS = b"\x11"
PAYLOAD_AND_HEADER = b"\x26"
HEADER_CRC = b"\x4a\x8f"


CUBESAT_ID = b"\x11\x00\x00\x00\x00\x00\x00\x00"
GS_ID = b"\x00\x00\x00\x00\x00\x00\x00\x00"
CAPABILITY_FLAGS = b"\x00\x00\x00\x00\x00\x00\x00\x00"
SESSION_ID = b"\x01\x00\x00\x00\x00\x00\x00\x00"
AIRMAC_PROTOCOL_VERSION = b"\x01\x00"

CRC_32 = b"\x3d\x90\x20\x8f"

PAYLOAD_BYTES = (
    AIRMAC_PROTOCOL_ID
    + RADIO_MODULE_ADDRESS
    + PAYLOAD_AND_HEADER
    + HEADER_CRC
    + CUBESAT_ID
    + GS_ID
    + CAPABILITY_FLAGS
    + SESSION_ID
    + AIRMAC_PROTOCOL_VERSION
)


class AsyncUDPManager:
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

    async def write(self, data):
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


async def rx_consumer(phy: AsyncUDPManager):
    while True:
        data = await phy.read()
        print(f"Received: {data!r}")
        await phy.write("pong")


async def tx_initial(phy: AsyncUDPManager, interval: float = 2):
    payload = "hi"
    await phy.write(payload)
    await asyncio.sleep(interval)


async def tx_triage(phy: AsyncUDPManager, interval: float = 2):
    payload = "oh hi"
    await phy.write(payload)
    await asyncio.sleep(interval)


async def tx_response(phy: AsyncUDPManager, interval: float = 2):
    payload = "wasg"
    await phy.write(payload)
    await asyncio.sleep(interval)


async def mac_task(phy):
    while True:
        frame = await phy.read()

        # decide what to do
        print(f"frame: {frame}")
        if frame == b"\x02hi":
            await phy.write("oh hi")

        elif frame == b"\x05oh hi":
            await phy.write("wasg")
        elif frame == b"\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08":
            print("AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")


async def mac_beacon(phy):
    while True:
        await phy.write(b"\x08")
        await asyncio.sleep(1)


async def main(
    rx_port: tuple[str, int], tx_addr: tuple[str, int], *, send: bool
) -> None:
    phy = AsyncUDPManager(rx_port=rx_port, tx_addr=tx_addr)
    await phy.initialize()

    if send:
        # asyncio.create_task(mac_beacon(phy))
        await asyncio.create_task(mac_beacon(phy))

    else:
        await asyncio.sleep(3)
        frame = await phy.read()

        # decide what to do
        print(f"frame: {frame}")

    # asyncio.create_task(mac_task(phy))

    await asyncio.Event().wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rx-port", type=int)
    parser.add_argument("--tx-port", type=int)
    parser.add_argument("--send", action="store_true", default=False)
    parser.add_argument("--tx-ip", type=str, default="127.0.0.1")
    parser.add_argument("--rx-ip", type=str, default="127.0.0.2")
    args = parser.parse_args()
    asyncio.run(
        main((args.rx_ip, args.rx_port), (args.tx_ip, args.tx_port), send=args.send)
    )
