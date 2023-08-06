from typing import Callable

def trapezoidal_rule(f: Callable, a: int, b: int, n: int):
    h = (b - a) / n
    s = (f(a) + f(b)) / 2
    for i in range(1, n):
        s +=  f(a + i * h)
    return h * s