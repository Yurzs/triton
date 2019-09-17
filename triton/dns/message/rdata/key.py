
class KEY:
    class _Binary:
        def __init__(self, key: 'KEY'):
            self.key = key

        @property
        def full(self):
            result = bin(self.key.flags)[2:].zfill(16)
            result += bin(self.key.protocol)[2:].zfill(8)
            result += bin(self.key.algorithm)[2:].zfill(8)
            row = self.key.public_key.decode()
            res = ''.join([bin(i)[2:].zfill(8) for i in [ord(c) for c in row]])
            result += res
            return result

    id = 1

    def __init__(self, answer):
        self.answer = answer
        self.Binary = self._Binary(self)

    @classmethod
    async def parse_bytes(cls, answer, read_len):
        instance = cls(answer)
        instance.flags = answer.message.stream.read(f'bin:16')
        instance.protocol = answer.message.stream.read(f'uint:8')
        instance.algorithm = answer.message.stream.read(f'uint:8')
        str_ = answer.message.stream.read(f'bin:{read_len - 4}')
        instance.public_key = ''.join([chr(int(x, base=2)) for x in [str[i:i + 8] for i in range(0, len(str_), 8)]])
        return instance

    @classmethod
    async def parse_dict(cls, answer, data):
        instance = cls(answer)
        instance.flags = data.get('flags')
        instance.protocol = 3
        instance.algorithm = data.get('algorithm')
        instance.public_key = data.get('public_key')
        return instance

    @property
    def __dict__(self):
        return {'flags': int(self.flags),
                'protocol': int(self.protocol),
                'algorithm': int(self.algorithm),
                'public_key': str(self.public_key)}