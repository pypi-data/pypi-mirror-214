from typing import Callable

def trapezoidal_rule(f: Callable, a: float, b: float, n: float) -> float:
    h = (b - a) / n
    s = (f(a) + f(b)) / 2
    for i in range(1, n):
        s +=  f(a + i * h)
    return h * s


def three_eights_rule(f: Callable, a: float, b: float, n: float) -> float:
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        if i % 3 == 0:
            s += 2 * f(x)
        else:
            s += 3 * f(x)
    return (3 * h / 8) * s