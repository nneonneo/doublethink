"""
Format AA i mod op
M = AA + rI[i]
V = M[mod]
"""

def fspec(opcode):
	def fn(m, it, a):
		return [a / 64, a % 64, it, 8 * m[0] + m[1], opcode]
	return fn

def fixedspec(opcode, spec):
	def fn(it, a):
		return [a / 64, a % 64, it, spec, opcode]
	return fn

def LOAD_IMMEDIATE_A(imm):
	return [imm / 64, imm % 64, 5, 48, 2]

def LOAD_IMMEDIATE_i(imm, i):
	return [imm / 64, imm % 64, 5, 48 + i, 2]

LDA = fspec(8)
LDX = fspec(15)
LDi = lambda i: fspec(8 + i)
ADD = fspec(1)
SUB = fspec(2)
MUL = fspec(3)
DIV = fspec(4)

CMPA = fspec(56)
CMPX = fspec(63)
CMPi = lambda i: fspec(56 + i)
JMP  = fixedspec(39, 0)
JSJ  = fixedspec(39, 1)
JOV  = fixedspec(39, 2)
JNOV = fixedspec(39, 3)
JL   = fixedspec(39, 4)
JE   = fixedspec(39, 5)
JG   = fixedspec(39, 6)
JGE  = fixedspec(39, 7)
JNE  = fixedspec(39, 8)
JLE  = fixedspec(39, 9)

TYPE_IN  = fixedspec(36, 19)
TYPE_OUT = fixedspec(37, 19)

MOVE = lambda n: fixedspec(7, n)
NOP  = [0, 0, 0, 0, 0]
HLT  = [0, 0, 0, 2, 5]

def program(commands):
	out = []
	for command in commands:
		for byte in command:
			binned = bin(byte)[2:]
			out += "0"*(6-len(binned)) + binned

	return ''.join(out)
