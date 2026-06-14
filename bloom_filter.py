import math
import mmh3


class BloomFilter:

    def __init__(self, count, fp_rate, serializer):
        self.count = count
        self.fp_rate = fp_rate
        self.size = self.get_size(count, fp_rate)
        self.bit_array = [False] * self.size
        self.hash_count = self.get_hash_count(self.size, count)
        self.serializer = serializer

    @classmethod
    def get_size(cls, n, p):
        m = -(n * math.log(p) / math.log(2) ** 2)
        return int(m)

    @classmethod
    def get_hash_count(cls, m, n):
        k = (m / n) * (math.log(2))
        return int(k)

    def add(self, elem):
        serialized_elem = self.serializer(elem)
        for i in range(1, 1 + self.hash_count):
            digest = mmh3.hash(serialized_elem, i) % self.size
            self.bit_array[digest] = True

    def check(self, elem):
        serialized_elem = self.serializer(elem)
        for i in range(1, 1 + self.hash_count):
            digest = mmh3.hash(serialized_elem, i) % self.size
            if not self.bit_array[digest]: return False

        return True


bf = BloomFilter(10, 0.1, lambda x: x + '0000')
bf.add("apple")
bf.add("mango")
print(bf.check("app"))
print(bf.check("apple"))
print(bf.check("mango2"))
print(bf.check("mango"))
print(bf.check("mango3"))
