import argparse
import binascii
import re
import asyncio
import math
import socket
from typing import Optional
import struct

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

        self.read_queue = asyncio.Queue(8)
        self.write_queue = asyncio.Queue(8)

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
                # print(f"TX COMPLETED, sent {data}")
                await asyncio.sleep(0.1)

    async def _rx_loop(self):
        while True:
            try:
                data, addr = await asyncio.wait_for(
                    self.loop.sock_recvfrom(self._rx_sock, 65535), timeout=1
                )

                await self.read_queue.put(data)
                # hexdump(data)
            except asyncio.TimeoutError:
                print("T", flush=True, end="")
                # print(
                #     "#######################################################TIMEOUT ERROR WAITING FOR PING"
                # )
                
            except Exception as e:
                print(f"Read error: {e}")
                break

    async def write(self, data):
        await self.write_queue.put(gen_packet(data))
        # print("Successful Write to Queue from Airmac")

    async def read(self):
        data = await self.read_queue.get()
        # print(
        #     "#####################################################Retrieved data from Queue, pumping to Airmac. Recieved:"
        # )
        # hexdump(data)
        return data
    
    async def shutdown(self):
        print("Shutting down UDP manager...")

        # Cancel tasks
        tasks = [self._tx_task, self._rx_task]
        for t in tasks:
            if t:
                t.cancel()
                try:
                    await t
                except asyncio.CancelledError:
                    pass

        # Close sockets
        if self._tx_sock:
            self._tx_sock.close()
        if self._rx_sock:
            self._rx_sock.close()


def hexdump(data: bytes) -> None:
    hexstr = binascii.hexlify(data)
    hexstr = b" ".join(hexstr[i : i + 2] for i in range(0, len(hexstr), 2))
    text = re.sub(r"[^a-zA-Z]+".encode(), b".", data)
    # print(f"{hexstr} \t {text.decode()}")


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
    # print(f"crc 16: {crc16(frame).to_bytes(2, 'big')}")
    hexdump(frame)
    return b"\xaa" * 5 + b"\x7e" + frame + crc16(frame).to_bytes(2, "big")

def gen_airmac_header(data: str | bytes, protocol_id: bytes, length: bytes) -> bytes:
    
    proto_int = b""
    match protocol_id:
        case b"\x01":
            proto_int = b"\x01"
        case b"\x02": 
            proto_int = b"\x02"
        case b"\x03": 
            proto_int = b"\x03"
    
    print (f"{proto_int + b"\x11" + length + crc16(proto_int + b"\x11" + length).to_bytes(2, "little")}")
    print(f"{AIRMAC_PROTOCOL_ID + RADIO_MODULE_ADDRESS + PAYLOAD_AND_HEADER + HEADER_CRC}")
    return proto_int + b"\x11" + length + crc16(proto_int + b"\x11" + length).to_bytes(2, "little")


async def rx_consumer(phy: AsyncUDPManager):
    while True:
        data = await phy.read()
        # print(f"Received: {data!r}")
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


def decode_response_packet(data: bytes):
    AIRMAC_DATA = data[1:]
    if AIRMAC_DATA[0] ==  0x02:
        return True


###########################################TESTING FUNCTIONALITY###############################################

class Stats:
    def __init__(self) -> None:
        self.tx = 0
        self.rx = 0
    
    def reset(self) -> None:
        self.tx = 0
        self.rx = 0

    @property
    def pct_success(self) -> float:
        if self.rx == 0:
            return math.nan

        return self.tx / self.rx


async def stat_print_task(stats: Stats):
    stat_period = 2
    stat_deadline = time.monotonic() + stat_period
    while True:
        if time.monotonic() >= stat_deadline:
            print()
            print(f"# TXed : {stats.tx}")
            print(f"# RXed : {stats.rx}")
            print(f"# Ratio: {stats.pct_success}")
            print(f"{id(stats)}")
            stat_deadline = stat_deadline + stat_period

        await asyncio.sleep(stat_period // 4)
    

async def recieve_task(phy: AsyncUDPManager, stats: Stats):
    while True:
        frame = await phy.read()
        print("R", flush=True, end="")
        stats.rx += 1
        # print(f"frame: {frame}")
        # for b in frame:
        #     print(f"frame in Int = {b}")


ENCRYPTED_CAPTURED_HANDSHAKE_FRAME = (
    "51 a8 31 28 1e 48 06 81 05 47 6a 11 42 5f 1e d9 da 2c 74 8e 1b 64 a9 ef "
    "6b 66 64 3c 15 5d 61 7f 46 53 36 83 f5 1f 05 7c f2 ae f1 4d e7 5b f6 54"
)


DECRYPTED_CAPTURED_HANDSHAKE_FRAME = (
    "01 00 26 08 bf 01 00 22 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
    "00 00 00 00 00 00 00 00 00 03 00 00 00 00 00 00 00 95 6a 96 76"
)

RANDOM_BULLSHIT_HANDSHAKE_FRAME = (
    "26 fe f1 6e 90 a0 bc a5 6a fa f1 fe ce 45 2a 26 98 26 6d 24 d7 84 67 d4 64 03 db 11 76 71 76 9a 87 b5"
)

RANDOM_BULLSHIT_HANDSHAKE_FRAME_2 = (
    "26 fe f1 6e 90 a0 bc a5 6a fa f1 fe ce 45 2a 26 98 26 6d 24 d7 84 67 d4 64 03 a9 52 2b 03 0f 14 23 be 01 80 a7 75 9b"
)

CAPTURED_HANDSHAKE_PACKET = (
    "01 00 11 00 00 00 00 00 00 00 00 00 00 00 00 00 00 "
    "00 00 00 00 00 00 00 00 00 04 00 00 00 00 00 00 00"
)

AIRMAC_PROTOCOL_ID = b"\x01"
RADIO_MODULE_ADDRESS = b"\x11"
PAYLOAD_AND_HEADER = b"\x26"
HEADER_CRC = b"\x4a\x8f"

AIRMAC_PROTOCOL_VERSION = b"\x01\x00"
CUBESAT_ID = b"\x02\x00\x00\x00\x00\x00\x00\x00" #from read sat id command in SpaceDev
GROUND_STATION_ID = b"\x00\x00\x00\x00\x00\x00\x00\x00"
CAPABILITY_FLAGS = b"\x00\x00\x00\x00\x00\x00\x00\x00"
SESSION_ID = b"\x01\x00\x00\x00\x00\x00\x00\x00"


CRC_32_BYTE = 0xC073EA6C
CRC_32 = CRC_32_BYTE.to_bytes(4, byteorder="little")

RECONSTRUCTED_AIRMAC_INIT_HANDSHAKE_FRAME = (
    AIRMAC_PROTOCOL_ID
    + RADIO_MODULE_ADDRESS
    + PAYLOAD_AND_HEADER
    + HEADER_CRC
    + AIRMAC_PROTOCOL_VERSION
    + CUBESAT_ID
    + GROUND_STATION_ID
    + CAPABILITY_FLAGS
    + SESSION_ID
    +CRC_32
)

PAKCET_ID = b"\x01\x00\x00\x00\x00\x00\x00\x00"
PAYLOAD_PROTOCOL_TP = b"\x10"
SYNC_FRAME_FLAG = b"\x14" #10
HOST_CONTEXT = b"\x00\x00\x00\x00\x00\x00\x00\x00"
TARGET_SYSTEM_TYPE = b"\x02\x00"
TARGET_SYSTEM_ADDRESS = b"\x11\x00\x00\x00\x00\x00\x00\x00" #18
TARGET_LOCAL_ADDRESS = b"\x00\x00\x00\x00\x00\x00\x00\x00"
ENTIRE_TP_DATAGRAM_SIZE = b"\x01\x00\x00\x00" 


#Sync frame needs to be encapsulated by Airmac Frame
#Sync packet is 40 Bytes 
AIRMAC_TP_PROTOCOL_HEADER_ID = b"\x03"
TP_SYNC_FRAME = "03 11 2C 60 40 28 01 00 00 00 00 00 00 00 10 14 00 00 00 00 00 00 00 00 02 00 11 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 33 5E 07 6B"


#
f = 51 
TEST = ( f"{f:02x}")


async def send_task(phy: AsyncUDPManager, stats: Stats):
    count = 1
    while True:
        FRAME = bytes.fromhex(RECONSTRUCTED_AIRMAC_INIT_HANDSHAKE_FRAME.hex())
        await phy.write(FRAME)
        print(".", flush=True, end="")
        stats.tx += 1
        await asyncio.sleep(.1)




async def handshake_loop(phy: AsyncUDPManager, stats: Stats):
        """Continuously attempt handshake until success"""
        print("[GS] Starting handshake loop...")
        handshooken = 0
        while True:
            frame = bytes.fromhex(RECONSTRUCTED_AIRMAC_INIT_HANDSHAKE_FRAME.hex())
            while handshooken == 0:
                await phy.write(frame)
                stats.tx += 1
                print(".", end="", flush=True)

                try:
                    response = await asyncio.wait_for(phy.read(), timeout=2)

                    print(" [RX]", end="", flush=True)

                    if decode_response_packet(response):
                        print("\n[GS] Handshake successful ")
                        stats.rx += 1
                        handshooken = 1
                        sync = bytes.fromhex(TP_SYNC_FRAME)
                        await phy.write(sync)
                        stats.tx += 1
                        print(".", end="", flush=True)
                        return

                except asyncio.TimeoutError:
                    print(" [timeout]", end="", flush=True)
            
            

            await asyncio.sleep(0.5)

async def sync_spam(phy: AsyncUDPManager, stats: Stats):
    while True:
        sync = bytes.fromhex(TP_SYNC_FRAME)
        await phy.write(sync)
        print("#", end="", flush=True)
        await asyncio.sleep(.5)
        

##################################################################################################################


async def main(
    rx_port: tuple[str, int], tx_addr: tuple[str, int], *, send: bool
) -> None:
    stats = Stats()
    phy = AsyncUDPManager(rx_port=rx_port, tx_addr=tx_addr)
    await phy.initialize()


    gen_airmac_header( (AIRMAC_PROTOCOL_VERSION
    + CUBESAT_ID
    + GROUND_STATION_ID
    + CAPABILITY_FLAGS
    + SESSION_ID
    +CRC_32), b"\x01", b"\x26")
    tasks = [] 
    #tasks.append(asyncio.create_task(stat_print_task(stats)))
    #if send:
        # asyncio.create_task(mac_beacon(phy))
    #    tasks.append(asyncio.create_task(send_task(phy, stats)))

    #else:
    #   tasks.append(asyncio.create_task(recieve_task(phy, stats)))
    

    # asyncio.create_task(mac_task(phy))
    tasks.append(asyncio.create_task(handshake_loop(phy, stats)))
    tasks.append(asyncio.create_task(sync_spam(phy, stats)))

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
