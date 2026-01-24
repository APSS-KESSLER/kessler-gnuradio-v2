import asyncio


class UdpServerProtocol(asyncio.DatagramProtocol):
    def datagram_received(self, data, addr):
        print(f"Received {data} from {addr}")


async def main():
    loop = asyncio.get_running_loop()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UdpServerProtocol(),
        local_addr=("127.0.0.1", 2004),
    )

    print("UDP server listening on 2004")
    await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
