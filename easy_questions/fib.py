from functools import lru_cache
from typing import Dict


# base fib
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


# using memoization
memo: Dict[int, int] = {0: 0, 1: 1}


def fib2(n: int) -> int:
    if n not in memo:
        memo[n] = fib2(n - 1) + fib2(n - 2)
    return memo[n]


# or using decorator cache
@lru_cache(maxsize=None)
def fib3(n: int) -> int:
    if n < 2:
        return n
    return fib3(n - 1) + fib3(n - 3)


if __name__ == '__main__':
    print(fib3(55))
