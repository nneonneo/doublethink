from bitstr import BitString
import random
from mix_assem import *

# 30 bits
def build_jump(bs, jpos, tpos):
    assert jpos % 30 == 0
    assert tpos % 30 == 0

    bits = program([
        JMP(5, tpos // 30 + 100)
    ])
    bs.write_safe(jpos, 30, bits)

# 30 bits
def build_prog(bs, tpos):
    assert tpos % 30 == 0

    bits = program([
        TYPE_OUT(5, 3137),
    ])
    bs.write_safe(tpos, 30, bits)
