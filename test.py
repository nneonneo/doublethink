import lgp30
from bitstr import BitString, bytes_to_bits
import random

amd64 = open('shellcode.amd64', 'rb').read()

bs = BitString([None] * (512 * 8))
bs.write_safe(0, None, bytes_to_bits('\xeb\x71')) # [b]ring for 0x01
bs.write_safe(0x73 * 8, None, bytes_to_bits(amd64))
lgp30.build_jump(bs, 31, 31*2)
lgp30.build_prog(bs, 31*2)

out = ''
for i in xrange(0, len(bs), 8):
    out += chr(int(''.join(random.choice('01') if c is None else c for c in bs[i:i+8]), 2))

print out
