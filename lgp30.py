from bitstr import BitString
import random

instrs = 'zbyridnmpeuthcas'

prog = '''
b 1337   # 0000 bring 1337
y 0002+b # 0001 store addr portion to p instr
p 0000   # 0002 print argument
b 0000+b # 0003 bring initial instruction
a 0007+b # 0004 add [0007] = 0001
y 0000+b # 0005 store back to 0000
u 0000+b # 0006 jump to 0000
z 0001   # 0007 data to store
'''.strip()

def build_jump(bs, jpos, tpos):
    assert jpos % 31 == 0
    assert tpos % 31 == 0
    tmem = tpos // 31 + 64
    bs.write_safe(jpos + 12, 4, instrs.index('u'))
    bs.write_safe(jpos + 18, 6, tmem // 64)
    bs.write_safe(jpos + 24, 6, tmem % 64)

def build_prog(bs, tpos):
    assert tpos % 31 == 0
    tmem = tpos // 31 + 64
    for i, line in enumerate(prog.split('\n')):
        line = line.split('#')[0].strip()
        oppos = tpos + 31*i
        opcode, oparg = line.split()
        mhi = int(oparg[:2])
        mlo = int(oparg[2:4])
        maddr = (mhi * 64) + mlo
        if oparg.endswith('+b'):
            maddr += tmem
        if i == 7:
            bs.write_safe(oppos, 1, 0)
        bs.write_safe(oppos + 12, 4, instrs.index(opcode))
        bs.write_safe(oppos + 16, 2, 0)
        bs.write_safe(oppos + 18, 6, maddr // 64)
        bs.write_safe(oppos + 24, 6, maddr % 64)
        bs.write_safe(oppos + 30, 1, 0)

if __name__ == '__main__':
    bs = BitString([None] * 4096)
    build_jump(bs, 0, 31*20)
    build_prog(bs, 31*20)

    # print ''.join('z' if c is None else c for c in bs)

    out = ''
    for i in xrange(0, len(bs), 8):
        out += chr(int(''.join(random.choice('01') if c is None else c for c in bs[i:i+8]), 2))

    print out
