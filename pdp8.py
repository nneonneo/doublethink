import sys
prog = '''
00 tls:        6046   # wake up printer
01 cla cll:    7300   # clear AC and link
02 tad flag:   1214+b # grab flag address
03 dca 10:     3010   # deposit address of string to auto-index register 10
04 cla cll:    7300   # clear AC and link
05 tad i 10:   1410   # load character
06 sna:        7450   # skip if non-zero
07   hlt:      7402   # halt
10 tsf:        6041   # printer ready?
11   jmp .-1:  5010+b # no? loop!
12 tls:        6046   # yes? print!
13 jmp loop:   5004+b # get next char
14 <flag>:     1336
'''.strip()

def build_prog(bs, tpos):
    assert tpos % 12 == 0

    taddr = tpos // 12 + 0100
    for i, line in enumerate(prog.split('\n')):
        line = line.split('#')[0].strip()
        op = line.split(':')[1].strip()
        val = int(op[:4], 8)
        if op.endswith('+b'):
            val += taddr
        print >> sys.stderr, oct(val)

        bs.write_safe(tpos + 12 * i, 12, val)
