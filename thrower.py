from pwn import *
import sys

args = sys.argv[1:]

if len(args) < 1:
	print("loader.py <file.mix> <arches> <ipaddr>")
	sys.exit(1)

if len(args) < 2:
	arches = ["arm64", "lgp-30", "mix", "pdp-8"]
else:
	arches = args[1].split(",")

if len(args) < 3:
	ip = "127.0.0.1"
else:
	ip = args[2]

with open(args[0]) as program:
	contents = program.read()
	contents+= 'a'*(4096-len(contents))


tube = remote(ip, 9318)
def snd(d, rduntil=None):
	if rduntil is None:
		sys.stdout.write(tube.recv(timeout=0.4))
	else:
		sys.stdout.write(tube.recvuntil(rduntil))
	sys.stdout.flush()
	tube.send(d)
	sys.stdout.write(d)
	sys.stdout.flush()
def sndln(d, rduntil=None):
	snd(d+"\n", rduntil)

snd(contents)
sndln("", ">")
for arch in arches:
	sys.stdout.write(tube.recvuntil("next?"))
	sndln(arch, ">")
sndln("EOF", "next?")