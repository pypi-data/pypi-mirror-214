from typing import Callable, Optional
import sympy as sp
import numpy as np


class Integrate:
    def __init__(
        self, f: Callable, a: float, b: float, n: int, h: Optional[float] = None
    ) -> None:
        self.f = f
        self.a = a
        self.b = b
        self.n = n
        self.h = h
        if h is None:
            self.h = (self.b - self.a) / self.n

    def trapezoidal_rule(self) -> float:
        s = (self.f(self.a) + self.f(self.b)) / 2
        for i in range(1, self.n):
            s += self.f(self.a + i * self.h)
        return self.h * s

    def three_eights_rule(self) -> float:
        s = self.f(self.a) + self.f(self.b)
        for i in range(1, self.n):
            x = self.a + i * self.h
            if i % 3 == 0:
                s += 2 * self.f(x)
            else:
                s += 3 * self.f(x)
        return (3 * self.h / 8) * s

    @staticmethod
    def cotes_coef(i: int, m: int):
        a, b = sp.symbols("a b")
        formulas_dict = {
            1: {
                0: (b - a) / 2,
            },
            2: {
                0: (b - a) / 6,
                1: 4 * (b - a) / 6,
            },
            3: {
                0: (b - a) / 8,
                1: 3 * (b - a) / 8,
            },
            4: {
                0: 7 * (b - a) / 90,
                1: 16 * (b - a) / 45,
                2: 2 * (b - a) / 15,
            },
            5: {
                0: 19 * (b - a) / 288,
                1: 25 * (b - a) / 96,
                2: 25 * (b - a) / 144,
            },
            6: {
                0: 41 * (b - a) / 840,
                1: 9 * (b - a) / 35,
                2: 9 * (b - a) / 280,
                3: 34 * (b - a) / 105,
            },
        }
        if i > m / 2:
            return Integrate.cotes_coef(m - i, m)
        return formulas_dict[m][i]

    def cotes_rule(self, x_values: np.ndarray, f_x_values: np.ndarray) -> float:
        a, b = sp.symbols("a b")
        L5_integr = np.sum(
            [
                Integrate.cotes_coef(i, len(x_values)) * f_x_values[i]
                for i in range(len(x_values))
            ]
        )
        return L5_integr.subs({a: x_values[0], b: x_values[-1]})

    def simpson_rule(self) -> float:
        simpson_integral = 0

        for step in range(self.n):
            x1 = self.a + step * self.h
            x2 = self.a + (step + 1) * self.h

            simpson_integral += (
                (x2 - x1)
                / 6.0
                * (self.f(x1) + 4.0 * self.f(0.5 * (x1 + x2)) + self.f(x2))
            )

        return simpson_integral

    def rectangles_rule(self, rect_type="middle") -> float:
        rectangles_integral = 0
        if rect_type == "left":
            for i in range(0, self.n):
                x_i_plus_1 = self.a + (i + 1) * self.h
                x_i = self.a + i * self.h
                f_x = self.f(x_i)
                rectangles_integral += f_x * (x_i_plus_1 - x_i)
        elif rect_type == "right":
            for i in range(1, self.n + 1):
                x_i = self.a + i * self.h
                x_i_minus_1 = self.a + (i - 1) * self.h
                f_x = self.f(x_i)
                rectangles_integral += f_x * (x_i - x_i_minus_1)
        elif rect_type == "middle":
            for i in range(0, self.n):
                x_i = self.a + (i * self.h)
                x_i_plus_1 = self.a + ((i + 1) * self.h)
                f_x = self.f((x_i + x_i_plus_1) / 2)
                rectangles_integral += f_x * (x_i_plus_1 - x_i)
        else:
            print("Correct options:\nleft\nright\nmiddle")
        return rectangles_integral
