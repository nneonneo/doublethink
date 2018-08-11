def bytes_to_bits(data):
    return BitString(''.join('{:08b}'.format(ord(c)) for c in data))

class BitString(list):
    def write_safe(self, pos, size, value):
        if isinstance(value, (int, long)):
            value = '{:0{width}b}'.format(value & ((1 << size) - 1), width=size)
        elif not size:
            size = len(value)
        if not all(v is None or v == value[i] for i,v in enumerate(self[pos:pos+size])):
            raise ValueError("attempted write to position %d of %s already has value %s" % (pos, value, self[pos:pos+size]))
        self[pos:pos+size] = value

    @staticmethod
    def repr(bs):
        return ''.join('z' if v is None else v for v in bs)
