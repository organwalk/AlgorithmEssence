# DNA搜索问题
# 一个字母代表一个核苷酸
# 三个字母代表一个密码子，密码子的编码决定了氨基酸的种类，而多个氨基酸合成蛋白质
from enum import IntEnum
from typing import Tuple, List


# 存储DNA
class Nucleotide(IntEnum):
    A = 1
    C = 2
    G = 3
    T = 4


# 密码子
Codon = Tuple[Nucleotide, Nucleotide, Nucleotide]
# 基因就是一连串密码子列表
Gene = List[Codon]
# 基因序列
gene_str: str = "ACGTGGCTCTCTAACGTACGTACGTACGGGGTTTATATATACCCTAGGACTCCCTTT"


# 字符串转为基因
def string_to_gene(s: str) -> Gene:
    gene: Gene = []
    for i in range(0, len(s), 3):
        if (i + 2) >= len(s):
            return gene
        codon: Codon = (Nucleotide[s[i]], Nucleotide[s[i + 1]], Nucleotide[s[i + 2]])
        gene.append(codon)
    return gene


my_gene: Gene = string_to_gene(gene_str)  # 基因序列转为基因
acg: Codon = (Nucleotide.A, Nucleotide.C, Nucleotide.G)  # 测试用例ACG
gat: Codon = (Nucleotide.G, Nucleotide.A, Nucleotide.T)  # 测试用例GAT


# 线性搜索
def linear_search(gene: Gene, key_codon: Codon):
    for codon in gene:
        return codon == key_codon


def test_linear():
    print("Linear ACG:{}".format(linear_search(my_gene, acg)))  # True
    print("Linear GAT:{}".format(linear_search(my_gene, gat)))  # False


def binary_search(gene: Gene, key_codon: Codon):
    left: int = 0
    right: int = len(gene) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if gene[mid] < key_codon:
            left = mid + 1
        elif gene[mid] > key_codon:
            right = mid - 1
        else:
            return True
    return False


def test_binary():
    sorted_gene: Gene = sorted(my_gene)
    print("Binary ACG:{}".format(binary_search(sorted_gene, acg)))
    print("Binary GAT:{}".format(binary_search(sorted_gene, gat)))


if __name__ == '__main__':
    test_linear()
    test_binary()
