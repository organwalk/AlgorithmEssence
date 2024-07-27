# 核苷酸包括A、G、C、T，如果使用str类型存储，则每个字符需要8个二进制位存储
# 如果A->00 C->01 G->10 T->11 以该二进制存储（由八个二进制位减少为两个），则大幅压缩空间
from sys import getsizeof


class CompressedGene:
    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        self.bit_string: int = 1
        for nucleotide in gene.upper():
            self.bit_string <<= 2  # 每次循环都向左移两位，新的核苷酸存储在末尾
            if nucleotide == "A":
                self.bit_string |= 0b00
            elif nucleotide == "C":
                self.bit_string |= 0b01
            elif nucleotide == "G":
                self.bit_string |= 0b10
            elif nucleotide == "T":
                self.bit_string |= 0b11
            else:
                raise ValueError("不包含此值:{}".format(nucleotide))

    def decompress(self) -> str:
        gene: str = ""
        for i in range(0, self.bit_string.bit_length() - 1, 2):
            bits: int = self.bit_string >> i & 0b11
            if bits == 0b00:
                gene += "A"
            elif bits == 0b01:
                gene += "C"
            elif bits == 0b10:
                gene += "G"
            elif bits == 0b11:
                gene += "T"
            else:
                raise ValueError("不包含此值:{}".format(bits))
        return gene[::-1]

    def __str__(self) -> str:
        return self.decompress()


# original:8649 bytes
# compress:2320 bytes
if __name__ == '__main__':
    original: str = "TAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATATAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATA" * 100
    print("original:{} bytes".format(getsizeof(original)))
    compressed: CompressedGene = CompressedGene(original)
    print("compress:{} bytes".format(getsizeof(compressed.bit_string)))
    print(compressed)
    print("the same:{}".format(original == compressed.decompress()))
