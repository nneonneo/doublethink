import lgp30
import mix
import nova
import pdp8
import pdp10
from bitstr import BitString, bytes_to_bits
import random
import struct
import sys

amd64 = open('shellcode.amd64', 'rb').read()

bs = BitString([None] * (4096 * 8))
# jmp for PDP-8
bs.write_safe(0, 3, 5)
# jmp for LGP-30
bs.write_safe(12, 4, 0xa)
# nop for amd64
bs.write_safe(16, 2, 0)
# nop for MIX and add for arm64 and jmp addr for LGP-30
bs.write_safe(24, 6, 11)
# jmp for PDP-10 (pending)
#bs.write_safe(36*5, 36, 0254200000000) # hlt
bs.write_safe(36*5, 36, 0324000001212)

# jmp address for PDP-8
bs.write_safe(3, 9, 0540) # indirect read @0140
# jmp address for LGP-30
bs.write_safe(18, 6, 5)
# jmp for PDP-1
bs.write_safe(18*2, 18, 0622554)

# program for LGP-30
lgp30.build_prog(bs, 31*(64*(5-1)+11)) # @1984 for 248

# protect nova
bs.write_safe(32, 4, 0) # other combinations may be possible
nova_tpos = 3200
bs.write_safe(16 * (0225 - 0100), 16, nova_tpos//16 + 0100)
nova.build_prog(bs, nova_tpos)

# mix nops
bs.write_safe(30+24, 6, 7)
bs.write_safe(30+30, 4, 0x5)
bs.write_safe(30+34, 8, 0x7e) # x86-64 jump
bs.write_safe(60+24, 6, 0)
bs.write_safe(90+24, 6, 0)
mix.build_prog(bs, 120)

# code for x64
bs.write_safe(0x87*8, None, bytes_to_bits('\xe8' + struct.pack('<I', 0x480)))
bs.write_safe((0x87+0x480+0x5)*8, None, bytes_to_bits(open('shellcode.amd64', 'rb').read()))

# jmp for clemency
bs.write_safe(0x08*9, 9, 0b100000001)
bs.write_safe(0x09*9, 9, 0b110000000)
bs.write_safe(0x0a*9, 9, 0x031)

# clemency
bs.write_safe((((0x1 << 9) | 0x31) + 0x8) * 9, None, bytes_to_bits(open('shellcode.clemency', 'rb').read()))

# program for PDP-10
pdp10.build_prog(bs, 36*(01212-64))

print >> sys.stderr, bs[71], bs[73]
print >> sys.stderr, BitString.repr(bs)

out = ''
for i in xrange(0, len(bs), 1):
    out += str(int(''.join(random.choice('01') if c is None else c for c in bs[i:i+1]), 2))
    if i % 9 == 8: out += ' '
print >> sys.stderr, out

# program for PDP-8
bs.write_safe(12*040, 12, 0141)
pdp8.build_prog(bs, 12*041) # @384 for 180

bs.write_safe((02554-64)*18, None, '010011000000111111100100000000111111110110010000111111111011000000000011110110010000111111111011000000000011110110010000111111111011000000000011110000000001000000000000')

out = ''
for i in xrange(0, len(bs), 8):
    out += chr(int(''.join(random.choice('01') if c is None else c for c in bs[i:i+8]), 2))

print out
