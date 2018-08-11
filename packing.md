Bit packing!

# Present

## amd64

Little-endian, variable-length (byte-unit) instructions, code at 0x1337000, flag at ./flag.

## arm64

Little-endian, 32-bit instructions, code at 0x1337000, flag at ./flag.

## mipsel

Little-endian, 32-bit instructions, code at 0x1337000, flag at ./flag.

# Past

Bitstreams are all big-endian.

## ibm-1401

Variable-length (7-bit units) instructions, code at 0, flag at 900.

## lgp-30

31-bit words, code at 64, flag at 869

Does not appear to care about its first 12 bits at all - so can rewrite those arbitrarily!

```
0100: b 1337 # bring 1337
0101: y 0102 # store addr portion to p instr
0102: p 0000 # print argument
0103: b 0100 # bring initial instruction
0104: a 0107 # add [0107] = 0001
0105: c 0100 # store back to 0100
0106: u 0100 # jump to 0100
0107: x 0001
```

NOT PICKY - All instructions are defined, and only instruction 0 (halt) is particularly bad.

## mix

30-bit words, code at 100, flag at 3137

## nova

16-bit words, code at 0100, flag at 01337.

## pdp-1

18-bit words, code at 64, flag at 0

## pdp-8

12-bit words, code at 64, flag at 01337

## pdp-10

36-bit words, code at 64, flag at 01337

# Future

## Clemency

Big-endian 27-bit words, middle nyte first, then MSN, then LSN. Code at 0x0000000, flag at 0x4010000.

First byte is going to be rA/rB for most instructions - should be fairly easy to have pseudo-nops. Misalignment should help.

## Hexagon

Little-endian 32-bit words? Code at 0x10000, flag at ./flag?

## mmix

64-bit words, code at 0x200, flag in ./flag?

## Risc-V

Little-endian, variable-length (16-bit unit) instructions, code at 0x1337000, flag at ./flag.
