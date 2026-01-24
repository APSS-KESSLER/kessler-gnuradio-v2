import asyncio

UDP_TX_IP = "127.0.0.1"
UDP_TX_PORT = 2004


class UdpClientProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport
        print("UDP connection ready")

        # Send data
        self.transport.sendto(b"Hello", (UDP_TX_IP, UDP_TX_PORT))

    def error_received(self, exc):
        print("Error received:", exc)

    def connection_lost(self, exc):
        print("Connection closed")


async def main():
    loop = asyncio.get_running_loop()
    while 1:
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: UdpClientProtocol(),
            remote_addr=(UDP_TX_IP, UDP_TX_PORT),
        )

    await asyncio.sleep(5)
    transport.close()


if __name__ == "__main__":
    asyncio.run(main())
