import csv
from typing import List
from util import normalize_by_feature_scaling
from network import Network
from random import shuffle


def iris_interpret_output(output: List[float]) -> str:
    # 如果最大值是第一个元素，则说明预测的物种是 "Iris-setosa"
    if max(output) == output[0]:
        return "Iris-setosa"

    # 如果最大值是第二个元素，则说明预测的物种是 "Iris-versicolor"
    elif max(output) == output[1]:
        return "Iris-versicolor"

    # 否则，预测的物种是 "Iris-virginica"
    else:
        return "Iris-virginica"


if __name__ == "__main__":
    # 初始化存储数据的列表
    iris_parameters: List[List[float]] = []  # 存储鸢尾花数据的特征值
    iris_classifications: List[List[float]] = []  # 存储鸢尾花数据的分类标签
    iris_species: List[str] = []  # 存储鸢尾花的物种标签

    # 打开 'iris.csv' 文件进行读取
    with open('iris.csv', mode='r') as iris_file:
        # 使用 csv.reader 读取文件内容，并将其转换为列表
        irises: List = list(csv.reader(iris_file))

        # 随机打乱数据行的顺序
        shuffle(irises)

        # 遍历每一行数据
        for iris in irises:
            # 提取前四列（特征值）并将其转换为浮点数
            parameters: List[float] = [float(n) for n in iris[0:4]]
            iris_parameters.append(parameters)  # 将特征值添加到 iris_parameters 列表中

            # 提取第五列（物种标签）
            species: str = iris[4]

            # 将物种标签转换为分类标签的 one-hot 编码
            if species == "Iris-setosa":
                iris_classifications.append([1.0, 0.0, 0.0])
            elif species == "Iris-versicolor":
                iris_classifications.append([0.0, 1.0, 0.0])
            else:
                iris_classifications.append([0.0, 0.0, 1.0])

            # 将物种标签添加到 iris_species 列表中
            iris_species.append(species)

    # 对特征值进行归一化处理
    normalize_by_feature_scaling(iris_parameters)

    iris_network: Network = Network([4, 6, 3], 0.3)

    # 从 iris_parameters 中提取前 140 个样本作为训练数据
    iris_trainers: List[List[float]] = iris_parameters[0:140]

    # 从 iris_classifications 中提取前 140 个样本的正确分类标签作为训练数据的标签
    iris_trainers_corrects: List[List[float]] = iris_classifications[0:140]

    # 进行 50 次训练迭代
    for _ in range(50):
        # 使用提取的训练数据和正确分类标签训练神经网络
        iris_network.train(iris_trainers, iris_trainers_corrects)

    # 从 iris_parameters 中提取第 141 到第 150 个样本作为测试数据
    iris_testers: List[List[float]] = iris_parameters[140:150]

    # 从 iris_species 中提取第 141 到第 150 个样本的实际分类标签作为测试数据的标签
    iris_testers_corrects: List[str] = iris_species[140:150]

    # 使用测试数据和实际分类标签对训练好的神经网络进行验证
    # iris_interpret_output 用于将神经网络的输出概率转换为具体的物种名称
    iris_results = iris_network.validate(iris_testers, iris_testers_corrects, iris_interpret_output)

    # 打印验证结果：正确分类的数量，总的测试样本数量，以及分类准确率（以百分比表示）
    print(f"{iris_results[0]} correct of {iris_results[1]} = {iris_results[2] * 100}%")

