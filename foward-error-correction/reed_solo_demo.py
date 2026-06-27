# Note: All the below code was ripped from https://pypi.org/project/reedsolo/

# Initialization
from reedsolo import RSCodec
rsc = RSCodec(10)  # 10 ecc symbols

# Encoding
# just a list of numbers/symbols:
tx_msg = rsc.encode(bytearray([1,2,3,4]))
print(f"OG BYTE ARRAY: {tx_msg}")

# Decoding (repairing), here I have replaced some bits with 00 as errors.
# I am unsure of how exactly this will interface with hardware and GNU radio, 
# if there is a constant sample rate to make bytes then my model here for an error
# should be usable in real data (as byte array length and indicies don't change).
rx_msg = rsc.decode(b'\x00\x00\x00\x00,\x00\x1c+=\xf8h\xfa\x98M')

# PARTS OF THE rx_msg OUTPUT:
# 1. the decoded (corrected) message,
# 2. the decoded message and error correction code (which is itself also corrected)
# 3. the list of positions of the errata (errors and erasures)
print(f"NEW BYTE ARRAY: {rx_msg}")