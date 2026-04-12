import subprocess
import threading

rxevent = threading.Event()
txevent = threading.Event()
txcount = rxcount = 0

def ping():
    global txcount
    proc = subprocess.Popen(
        [
            "python",
            "./async-ping-pong.py",
            "--tx-port",
            "2000",
            "--rx-port",
            "2001",
            "--tx-ip",
            "127.0.0.2",
            "--send",
        ],
        stdout=subprocess.PIPE,
        text=True,
    )

    try:
        for line in proc.stdout:
            if line.startswith("# TXed"):
                txcount = int(line.split(":")[-1].strip())
                txevent.set()
    finally:
        proc.kill()
        proc.wait()

def pong():
    global rxcount
    proc = subprocess.Popen(
        [
            "python",
            "./async-ping-pong.py",
            "--tx-port",
            "2002",
            "--rx-port",
            "2003",
            "--rx-ip",
            "127.0.0.1",
        ],
        stdout=subprocess.PIPE,
        text=True,
    )

    try:
        for line in proc.stdout:
            if line.startswith("# RXed"):
                rxcount = int(line.split(":")[-1].strip())
                rxevent.set()
    finally:
        proc.kill()
        proc.wait()


pinger = threading.Thread(target=ping)
ponger = threading.Thread(target=pong)

pinger.start()
ponger.start()

while True:
    txevent.wait()
    txevent.clear()
    rxevent.wait()
    rxevent.clear()
    print(f"# TX:    {txcount}")
    print(f"# RX:    {rxcount}")
    print(f"# RX/TX: {(rxcount / txcount)*100:.2f}%")

# # txer
# # rxer
# python ./async-ping-pong.py --tx-port 2002 --rx-port 2003 --rx-ip "127.0.0.1" &

# wait
