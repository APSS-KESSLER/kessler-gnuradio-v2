"""Test file for Rx side processing"""

import argparse
import binascii
import re
import socket
import sys
import time

# From ES UHF II USER MANUAL 2023
UHF_PRE_PAYLOAD = 7  # Preamble + Sync + Payload Length
UHF_POST_PAYLOAD = -2  # CRC


def hexdump(data: bytes) -> None:
    hexstr = binascii.hexlify(data)
    hexstr = b" ".join(hexstr[i : i + 2] for i in range(0, len(hexstr), 2))
    text = re.sub(r"[^a-zA-Z]+".encode(), b".", data)
    print(f"{hexstr} \t {text.decode()}")


def run_ping_pong(
    tx: socket.socket,
    rx: socket.socket,
    *,
    send: bool,
    tx_addr: tuple[str, int],
) -> None:
    while True:
        if send:
            tx.sendto(gen_packet("PING"), tx_addr)

            # RX
            rx.settimeout(1)
            try:
                data, _ = rx.recvfrom(1024)
                hexdump(data)
            except TimeoutError:
                print("RX timeout while waiting for PONG")
                continue

            if not data:
                print("RX EOF Reached", file=sys.stderr)
                break

        else:
            data, _ = rx.recvfrom(1024)
            hexdump(data)
            tx.sendto(gen_packet("PONG"), tx_addr)


def main(rx_port: int, tx_addr: tuple[str, int], *, send: bool) -> None:
    """Main function to start the UDP server. Endurostack entrypoint."""
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("", rx_port))
    print(f"UDP RX on 0.0.0.0:{rx_port}")
    tx_ip, tx_port = tx_addr
    print(f"UDP TX on {tx_ip}:{tx_port}")

    try:
        run_ping_pong(udp_socket_tx, udp_socket, send=send, tx_addr=tx_addr)
    finally:
        udp_socket_tx.close()
        udp_socket.close()


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
    return b"\xaa" * 5 + b"\x7e" + frame + crc16(frame).to_bytes(2, "big")


def decode_packet(data: bytes) -> bytes:
    data = data[7:-2]
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rx-port", type=int)
    parser.add_argument("--tx-port", type=int)
    parser.add_argument("--send", action="store_true", default=False)
    parser.add_argument("--tx-ip", type=str, default="127.0.0.1")
    args = parser.parse_args()
    main(args.rx_port, (args.tx_ip, args.tx_port), send=args.send)
