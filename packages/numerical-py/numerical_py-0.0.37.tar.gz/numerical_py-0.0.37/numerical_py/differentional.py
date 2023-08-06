from typing import Callable, Tuple, List


class DifferentialEquation:
    def __init__(
        self,
        f: Callable,
        iterations: int,
        h: float,
        x: float,
        y: float,
    ) -> None:
        self.f = f
        self.iterations = iterations
        self.h = h
        self.x = x
        self.y = y

    def euler(self) -> Tuple[float, float, List[Tuple[float, float]]]:
        history = [(self.x, self.y)]
        for i in range(self.iterations):
            self.y += self.h * self.f(self.x, self.y)
            self.x += self.h
            history.append((self.x, self.y))
        return (self.x, self.y), history

    def advanced_euler(self) -> Tuple[float, float]:
        history = [(self.x, self.y)]
        for i in range(self.iterations):
            f_res = self.f(self.x, self.y)
            y_temp = self.y + self.h * f_res
            f_temp = self.f(self.x + self.h, y_temp)
            self.y += (f_res + f_temp) / 2 * self.h
            self.x += self.h
            history.append((self.x, self.y))
        return (self.x, self.y), history
