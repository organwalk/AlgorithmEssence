# 计算π可以通过莱布尼茨公式实现。它断定以下无穷级数的收敛值等于 π：
# π = 4/1 − 4/3 + 4/5 − 4/7 + 4/9 − 4/11…
# 以上无穷级数的分子保持为 4，而分母则每次递增 2，并且对每一项的操作是加法和减法交替出现


def calculating_pi(n_terms: int) -> float:
    numerator: float = 4.0
    denominator: float = 1.0
    opration: float = 1.0   # 加减符号可以使用-1或1表示
    pi: float = 0.0
    for _ in range(n_terms):
        pi += opration * (numerator / denominator)
        denominator += 2.0
        opration *= -1.0
    return pi


if __name__ == '__main__':
    print(calculating_pi(1000000))
