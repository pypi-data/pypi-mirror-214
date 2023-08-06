from typing import Callable, Tuple


class DifferentialEquation:
    def __init__(
        self,
        f: Callable,
        df_dx: Callable,
        iterations: int,
        h: float,
        x: float,
        y: float,
    ) -> None:
        self.f = f
        self.df_dx = df_dx
        self.iterations = iterations
        self.h = h
        self.x = x
        self.y = y

    def euler(self) -> Tuple[float, float]:
        # print('[Шаг 0]', 'x =', self.x, ', y =', self.y)

        # for i in range(self.iterations):
        #     self.y += self.h * self.df_dx(self.x, self.y)
        #     self.x += self.h
        #     print('[Шаг', str(i + 1) + ']', 'x =', self.x, ', y =', self.y)

        # return round(self.x, 4), round(self.y, 4)
        raise NotImplementedError
