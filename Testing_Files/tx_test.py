import asyncio
import binascii
import re

UDP_TX_IP = "127.0.0.1"
UDP_TX_PORT = 2000
SEND_INTERVAL = 1.0  # seconds


# ---------------- CRC16 ----------------


def _generate_crc16_table(poly: int) -> list[int]:
    table = [0] * 256
    for i in range(256):
        crc = i << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFFFF
        table[i] = crc
    return table


CRC16_POLY = 0x1021
CRC16_TABLE = _generate_crc16_table(CRC16_POLY)


def crc16(data: bytes, init: int = 0xFFFF) -> int:
    crc = init
    for b in data:
        crc = CRC16_TABLE[((crc >> 8) ^ b) & 0xFF] ^ (crc << 8)
        crc &= 0xFFFF
    return crc


# ---------------- Packet ----------------


def gen_packet(payload: bytes) -> bytes:
    if len(payload) > 255:
        raise ValueError("Payload too large (max 255 bytes)")

    frame = bytes([len(payload)]) + payload
    crc = crc16(frame).to_bytes(2, "big")

    return b"\xaa" * 5 + b"\x7e" + frame + crc


# ---------------- Debug ----------------


def hexdump(data: bytes) -> None:
    hexstr = binascii.hexlify(data)
    hexstr = b" ".join(hexstr[i : i + 2] for i in range(0, len(hexstr), 2))
    text = re.sub(rb"[^ -~]", b".", data)
    print(f"{hexstr.decode()}    {text.decode()}")


# ---------------- UDP Protocol ----------------


class UdpClientProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print("UDP connection ready")

    def send_packet(self):
        payload = (
            b"\x01\x00\x26\x08\xbf\x01\x00\x11"
            b"\x00" * 24 + b"\x04\x00\x00\x00\x00\x00\x00\x00"
            b"\x95\x6a\x96\x76"
        )

        packet = gen_packet(payload)
        hexdump(packet)

        self.transport.sendto(packet, (UDP_TX_IP, UDP_TX_PORT))

    def error_received(self, exc):
        print("UDP error:", exc)

    def connection_lost(self, exc):
        print("UDP connection closed")


# ---------------- Main ----------------


async def main():
    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UdpClientProtocol(),
        remote_addr=(UDP_TX_IP, UDP_TX_PORT),
    )

    try:
        while True:
            protocol.send_packet()
            await asyncio.sleep(SEND_INTERVAL)
    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(main())
