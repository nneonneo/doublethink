import lgp30
import mix
import pdp8
from bitstr import BitString, bytes_to_bits
import random
import struct
import sys

amd64 = open('shellcode.amd64', 'rb').read()

bs = BitString([None] * (4096 * 8))
# bs.write_safe(0, None, bytes_to_bits('\xeb\x7a')) # [u]nconditional jump = 0xa for lgp30
# jmp for PDP-8
bs.write_safe(0, 3, 5)
# jmp for LGP-30
bs.write_safe(12, 4, 0xa)
# pseudo-nop for arm64
bs.write_safe(16, 2, 1)
# nop for MIX and add for arm64
bs.write_safe(24, 6, 2)
# jmp for PDP-10 (pending)
bs.write_safe(36*5, 36, 0254200000000)

# jmp address for PDP-8
bs.write_safe(3, 9, 0140)
# jmp address for LGP-30
bs.write_safe(18, 6, 2)
# jmp for PDP-1
bs.write_safe(18*2, 18, 0622554)

# program for LGP-30
lgp30.build_prog(bs, 31*(64+2)) # @1984 for 248

# mix nops
bs.write_safe(30+24, 6, 11)
bs.write_safe(60+24, 6, 0)
bs.write_safe(90+24, 6, 0)
mix.build_prog(bs, 120)

# jmp for clemency
bs.write_safe(0x0b*9, 9, 0b000000001)
bs.write_safe(0x0c*9, 9, 0b110000000)
bs.write_safe(0x0d*9, 9, 0x031)

# arm "and" instr
bs.write_safe(28, 4, 0xa)
bs.write_safe(32+28, 4, 0x7)
bs.write_safe(32, 24, 0xcc95b0)
offs = (0x200 - 8) >> 2
bs.write_safe(64, 32, struct.unpack('>I', struct.pack('<I', 0x14000000 + offs))[0])
bs.write_safe(0x200 * 8, None, bytes_to_bits(open('shellcode.arm64', 'rb').read()))

# clemency???
bs.write_safe((((0x1 << 9) | 0x31) + 0xb) * 9, None, bytes_to_bits(open('shellcode.clemency', 'rb').read()))

print >> sys.stderr, BitString.repr(bs)

out = ''
for i in xrange(0, len(bs), 1):
    out += str(int(''.join(random.choice('01') if c is None else c for c in bs[i:i+1]), 2))
    if i % 9 == 8: out += ' '
print >> sys.stderr, out

# program for PDP-8
pdp8.build_prog(bs, 12*040) # @384 for 180

bs.write_safe((02554-64)*18, None, '010011000000111111100100000000111111110110010000111111111011000000000011110110010000111111111011000000000011110110010000111111111011000000000011110000000001000000000000')

out = ''
for i in xrange(0, len(bs), 8):
    out += chr(int(''.join(random.choice('01') if c is None else c for c in bs[i:i+8]), 2))

print out
