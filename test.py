import lgp30
import mix
import pdp8
from bitstr import BitString, bytes_to_bits
import random
import struct
import sys

amd64 = open('shellcode.amd64', 'rb').read()

bs = BitString([None] * (512 * 8))
# bs.write_safe(0, None, bytes_to_bits('\xeb\x7a')) # [u]nconditional jump = 0xa for lgp30
# jmp for PDP-8
bs.write_safe(0, 3, 5)
# jmp for LGP-30
bs.write_safe(12, 4, 0xa)
# pseudo-nop for arm64
bs.write_safe(16, 2, 1)
# nop for MIX and add for arm64
bs.write_safe(24, 6, 2)

# jmp address for PDP-8
bs.write_safe(3, 9, 0140)
# jmp address for LGP-30
bs.write_safe(18, 6, 2)

# program for LGP-30
lgp30.build_prog(bs, 31*(64+2)) # @1984 for 248

# program for MIX
mix.build_prog(bs, 30)

# jump for arm64
bs.write_safe(60, 4, 0x01)
offs = (0x200 - 8) >> 2
bs.write_safe(64, 32, struct.unpack('>I', struct.pack('<I', 0x14000000 + offs))[0])
bs.write_safe(0x200 * 8, None, bytes_to_bits(open('shellcode.arm64', 'rb').read()))

# program for PDP-8
pdp8.build_prog(bs, 12*040) # @384 for 180

print >> sys.stderr, bs

out = ''
for i in xrange(0, len(bs), 8):
    out += chr(int(''.join(random.choice('01') if c is None else c for c in bs[i:i+8]), 2))

print out
