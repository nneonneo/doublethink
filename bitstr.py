def bytes_to_bits(data):
    return BitString(''.join('{:08b}'.format(ord(c)) for c in data))

class BitString(list):
    def write_safe(self, pos, size, value):
        if isinstance(value, (int, long)):
            value = '{:0{width}b}'.format(value & ((1 << size) - 1), width=size)
        elif not size:
            size = len(value)
        if any(v is not None for v in self[pos:pos+size]):
            raise ValueError("attempted write to position %d already has value %s" % (pos, self[pos:pos+size]))
        self[pos:pos+size] = value
