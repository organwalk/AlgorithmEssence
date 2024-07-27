# DNA搜索问题
# 一个字母代表一个核苷酸
# 三个字母代表一个密码子，密码子的编码决定了氨基酸的种类，而多个氨基酸合成蛋白质

from enum import IntEnum
from typing import Tuple, List

# 存储DNA
Nucleotide: IntEnum = IntEnum('Nucleotide', ('A', 'C', 'G', 'T'))
Codon = Tuple[Nucleotide, Nucleotide, Nucleotide]
Gene = List[Codon]

