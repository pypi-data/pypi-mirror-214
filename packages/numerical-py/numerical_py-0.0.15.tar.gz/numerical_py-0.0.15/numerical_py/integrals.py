from typing import Callable, Optional

class Integrate:

    def __init__(self, f: Callable, a: float, b: float, n: float, h: Optional[float] = None) -> None:
        self.f = f
        self.a = a
        self.b = b
        self.n = n
        self.h = h

    def trapezoidal_rule(self) -> float:
        h = (self.b - self.a) / self.n
        s = (self.f(self.a) + self.f(self.b)) / 2
        for i in range(1, self.n):
            s +=  self.f(self.a + i * h)
        return h * s
    
    def three_eights_rule(self) -> float:
        h = (self.b - self.a) / self.n
        s = self.f(self.a) + self.f(self.b)
        for i in range(1, self.n):
            x = self.a + i * h
            if i % 3 == 0:
                s += 2 * self.f(x)
            else:
                s += 3 * self.f(x)
        return (3 * h / 8) * s