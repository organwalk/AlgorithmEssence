from typing import List
from math import exp


def dot_product(xs: List[float], ys: List[float]) -> float:
    return sum(x * y for x, y in zip(xs, ys))


# 激活函数
def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + exp(-x))


# 激活函数的导数，用于反向传播计算梯度
def derivative_sigmoid(x: float) -> float:
    sig: float = sigmoid(x)
    return sig * (1 - sig)


def normalize_by_feature_scaling(dataset: List[List[float]]) -> None:
    # 遍历数据集中每一列（特征）
    for col_num in range(len(dataset[0])):
        # 提取当前列的所有值
        column: List[float] = [row[col_num] for row in dataset]

        # 计算当前列的最大值
        maximum = max(column)

        # 计算当前列的最小值
        minimum = min(column)

        # 对数据集中每一行的当前列进行归一化处理
        for row_num in range(len(dataset)):
            # 将当前值归一化为 [0, 1] 之间的值
            dataset[row_num][col_num] = (dataset[row_num][col_num] - minimum) / (maximum - minimum)
