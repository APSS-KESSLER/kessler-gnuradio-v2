"""Test file for Rx side processing"""

import argparse
import binascii
import re
import socket
import time

UDP_PORT_RX = 2001
UDP_PORT_TX = 2003
UDP_IP = "127.0.0.1"

# From ES UHF II USER MANUAL 2023
UHF_PRE_PAYLOAD = 7  # Preamble + Sync + Payload Length
UHF_POST_PAYLOAD = -2  # CRC


def main() -> None:
    """Main function to start the UDP server. Endurostack entrypoint."""
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket_tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("", UDP_PORT_RX))
    udp_socket_tx.bind(("", UDP_PORT_TX))
    print(f"UDP server listening on port {UDP_PORT_RX}")

    while True:
        data, addr = udp_socket.recvfrom(1024)
        if not data:
            print("Null value recieved")
            break
        message = data.decode("utf-8")
        print(f"RECIEVED: {message} from: {addr}")
        time.sleep(0.5)

        message = "PONG"
        message = message.encode("utf-8")
        data = gen_packet(message)
        print(f"Generated packet: {data}")
        # data = b"Hello, this is a test message!"
        udp_socket.send(data)
        # tcp_socket.sendto(data, (ADDR, PORT))
        print("== SENDING")
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


def gen_packet(data: bytes) -> bytes:
    """Gen packet."""
    frame = bytes([len(data), *data])
    return b"\xaa" * 5 + b"\x7e" + frame + crc16(frame).to_bytes(2, "big")


def decode_packet(data: bytes) -> bytes:
    data = data[7:-2]
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rx-port", type=int)
    parser.add_argument("--tx-port", type=int)
    parser.add_argument("--send-data")
    main()
