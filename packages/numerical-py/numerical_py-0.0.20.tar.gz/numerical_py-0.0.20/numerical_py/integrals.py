from typing import Callable, Optional

class Integrate:

    def __init__(self, f: Callable, a: float, b: float, n: int, h: Optional[float] = None) -> None:
        self.f = f
        self.a = a
        self.b = b
        self.n = n
        self.h = h

    def trapezoidal_rule(self) -> float:
        """
        def trapezoidal_rule(f: Callable, a: float, b: float, n: int, h: Optional[float] = None) -> float:
            if h is None:
                h = (b - a) / n
            s = (f(a) + (b)) / 2
            for i in range(1, n):
                s +=  f(a + i * h)
            return h * s
        """
        if self.h is None:
            self.h = (self.b - self.a) / self.n
        s = (self.f(self.a) + self.f(self.b)) / 2
        for i in range(1, self.n):
            s +=  self.f(self.a + i * self.h)
        return self.h * s
    
    def three_eights_rule(self) -> float:
        """
        def three_eights_rule(f: Callable, a: float, b: float, n: int, h: Optional[float] = None) -> float:
            if h is None:
                h = (b - a) / n
            s = f(a) + f(b)
            for i in range(1, n):
                x = a + i * h
                if i % 3 == 0:
                    s += 2 * f(x)
                else:
                    s += 3 * f(x)
            return (3 * h / 8) * s
        """

        if self.h is None:
            self.h = (self.b - self.a) / self.n
        s = self.f(self.a) + self.f(self.b)
        for i in range(1, self.n):
            x = self.a + i * self.h
            if i % 3 == 0:
                s += 2 * self.f(x)
            else:
                s += 3 * self.f(x)
        return (3 * self.h / 8) * s