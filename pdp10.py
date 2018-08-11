import sys
prog = '''
201040001337
201100000400 # <-- address A
200001000000
322000000113
202000000033
436100000033
700200012000
332000000033 # <-- address B
324000000007+b # <-- jump to B (replace 107)
271040000001
324000000002+b # <-- jump to A (replace 102)
254200000000 # HLT
'''.strip()

def build_prog(bs, tpos):
    assert tpos % 36 == 0

    taddr = tpos // 36 + 0100
    for i, line in enumerate(prog.split('\n')):
        op = line.split('#')[0].strip()
        val = int(op[:12], 8)
        if op.endswith('+b'):
            val += taddr

        bs.write_safe(tpos + 36 * i, 36, val)
