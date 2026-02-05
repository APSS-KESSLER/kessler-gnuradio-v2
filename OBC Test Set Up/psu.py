import argparse
import os
import sys

try:
    import serial
except ModuleNotFoundError:
    print("Missing dependency 'pyserial'")
    print("Please run 'py -3 -m pip install --user pyserial'\n")
    sys.exit()

try:
    import requests

    def notify(message: str) -> None:
        try:
            DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1276257261689245696/Eyg6RApIFTNpRz3K_7muDIdO8X5hSmzS9EKWShZpZPz2eczTTDnWkI-wrWoS2zjg0N-d?thread_id=1423579236513611787"
            r = requests.post(DISCORD_WEBHOOK, json={"content": message}, timeout=2)
            r.raise_for_status()
        except:
            print("Failed to send notification.")

except ModuleNotFoundError:
    print("Missing dependency 'requests'")
    print("Please run 'py -3 -m pip install --user requests'\n")

    def notify(message: str) -> None:
        pass


if os.name == "nt":
    port_default = "COM16"
else:
    port_default = "/dev/serial/by-id/usb-TDK-Lambda_Z+_Serial_Port_324B943-0002-if00"


parser = argparse.ArgumentParser(description="Enable or disable the PSU output.")

# there should be two commands that can be done: psu.py enable, and psu.py disable

parser.add_argument(
    "mode",
    choices=["enable", "disable", "toggle"],
    help="Enable or disable the PSU output.",
)
parser.add_argument(
    "--port", type=str, default=port_default, help="Serial port of the PSU."
)
# default to "toggle" if no args provided
argv = sys.argv[1:] or ["toggle"]
args = parser.parse_args(args=argv)

TIMEOUT = 1.0
BAUDRATE = 9600

notify("🔌 PSU notification test.")


with serial.Serial(args.port, timeout=TIMEOUT, baudrate=BAUDRATE) as psu:
    psu.write(b"instrument:nselect 1\r\n")

    should_enable = args.mode == "enable"

    # check the current power state to see if it needs to be toggled
    if args.mode == "toggle":
        # read the current output state
        psu.write(b"output:state?\r\n")
        state = psu.read(1)
        if state == b"0":
            # currently disabled, so enable
            should_enable = True

    # Disable output first to avoid transients during voltage/current change.
    psu.write(b"output:state 0\r\n")
    if should_enable:
        # 5V is the nominal voltage of the bus, 2A is the LUP limit of the EPS.
        psu.write(b":voltage 5.0\r\n")
        psu.write(b":current 2.0\r\n")
        psu.write(b"output:state 1\r\n")

        notify("🔌 PSU output enabled.")
    else:
        notify("🔌 PSU output disabled.")
