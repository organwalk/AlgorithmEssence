from __future__ import annotations
from typing import List, Callable, TypeVar, Tuple
from functools import reduce
from layer import Layer
from util import sigmoid, derivative_sigmoid

T = TypeVar('T')


class Network:
    def __init__(self, layer_structure: List[int], learning_rate: float,
                 activation_function: Callable[[float], float] = sigmoid,
                 derivative_activation_function: Callable[[float], float] = derivative_sigmoid) -> None:
        # 检查网络结构是否至少包含3层（输入层、隐藏层和输出层）
        if len(layer_structure) < 3:
            raise ValueError("Error: Should be at least 3 layers (1 input, 1 hidden, 1 output)")

        # 初始化一个空列表，用于存储网络中的所有层
        self.layers: List[Layer] = []

        # 创建输入层，前一层为None（因为输入层没有前一层）
        input_layer: Layer = Layer(None, layer_structure[0], learning_rate,
                                   activation_function, derivative_activation_function)
        # 将输入层添加到网络的层列表中
        self.layers.append(input_layer)

        # 遍历层结构中的其余层（隐藏层和输出层）
        for previous, num_neurons in enumerate(layer_structure[1:]):
            # 创建当前层，前一层为之前添加的层
            next_layer = Layer(self.layers[previous], num_neurons, learning_rate,
                               activation_function, derivative_activation_function)
            # 将当前层添加到网络的层列表中
            self.layers.append(next_layer)

    def outputs(self, o_input: List[float]) -> List[float]:
        return reduce((lambda inputs, layer: layer.outputs(inputs)), self.layers, o_input)

    def backpropagate(self, expected: List[float]) -> None:
        # 计算网络输出层的误差（delta）
        last_layer: int = len(self.layers) - 1
        self.layers[last_layer].calculate_deltas_for_output_layer(expected)

        # 从倒数第二层开始，逐层向前计算每一层的误差（delta）
        for i in range(last_layer - 1, 0, -1):
            # 计算隐藏层的误差（delta），需要使用下一层的误差
            self.layers[i].calculate_deltas_for_hidden_layer(self.layers[i + 1])

    def update_weights(self) -> None:
        # 遍历网络中的每一层，从第二层开始（跳过输入层）
        for layer in self.layers[1:]:
            # 遍历当前层的每个神经元
            for neuron in layer.neurons:
                # 遍历神经元的每个权重
                for w in range(len(neuron.weights)):
                    # 更新权重：当前权重 + (学习率 * 上一层的输出值 * 神经元的误差)
                    neuron.weights[w] = (neuron.weights[w] +
                                         (neuron.learning_rate * (layer.previous_layer.output_cache[w])
                                          * neuron.delta))

    def train(self, inputs: List[List[float]], expecteds: List[List[float]]) -> None:
        # 遍历所有训练样本
        for location, xs in enumerate(inputs):
            # 获取当前输入样本的期望输出（目标输出）
            ys: List[float] = expecteds[location]

            # 计算当前输入样本的网络输出
            outs: List[float] = self.outputs(xs)

            # 基于期望输出和实际输出进行反向传播，计算误差（delta）
            self.backpropagate(ys)

            # 更新所有神经元的权重
            self.update_weights()

    def validate(self, inputs: List[List[float]], expecteds: List[T],
                 interpret_output: Callable[[List[float]], T]) -> Tuple[int, int, float]:
        # 初始化正确预测的计数器
        correct: int = 0

        # 遍历所有输入样本及其对应的期望输出
        for input, expected in zip(inputs, expecteds):
            # 计算网络对当前输入样本的输出
            result: T = interpret_output(self.outputs(input))

            # 检查网络输出是否与期望输出匹配
            if result == expected:
                # 如果匹配，增加正确预测的计数器
                correct += 1

        # 计算正确预测的比例
        percentage: float = correct / len(inputs)

        # 返回正确预测的数量、总样本数量和预测准确率
        return correct, len(inputs), percentage

