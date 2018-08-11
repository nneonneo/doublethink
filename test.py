import lgp30
import mix
from bitstr import BitString, bytes_to_bits
import random

amd64 = open('shellcode.amd64', 'rb').read()

bs = BitString([None] * (512 * 8))
bs.write_safe(0, None, bytes_to_bits('\xeb\x7a')) # [u]nconditional jump = 0xa for lgp30
# nop for mix # XXXX oops there's something there already? it works so meh
# bs.write_safe(24, 6, 0)

lgp30.build_jump(bs, 0, 31*10)
lgp30.build_prog(bs, 31*10)

mix.build_jump(bs, 30, 30*20)
mix.build_prog(bs, 30*20)

bs.write_safe(0x7c * 8, None, bytes_to_bits(amd64))

out = ''
for i in xrange(0, len(bs), 8):
    out += chr(int(''.join(random.choice('01') if c is None else c for c in bs[i:i+8]), 2))

print out
