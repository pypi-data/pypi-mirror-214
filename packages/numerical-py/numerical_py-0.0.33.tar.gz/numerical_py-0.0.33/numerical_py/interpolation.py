import numpy as np
import sympy as sp


class Interpolate:
    def __init__(self, x_values: np.ndarray, f_x_values: np.ndarray) -> None:
        self.x_values = x_values
        self.f_x_values = f_x_values

    def classical(self, degree: int) -> np.ndarray:
        x = sp.symbols("x")

        def P(degree: int) -> sp.Function:
            x = sp.symbols("x")
            coeffs = sp.symbols(" ".join(["a" + str(i) for i in range(0, degree + 1)]))
            terms = [coeffs[0]] + [
                coeff * x ** (degree + 1) for degree, coeff in enumerate(coeffs[1:])
            ]
            return sum(terms)

        P_n_x = P(degree)
        linear_system = [
            (P_n_x - self.f_x_values[i]).subs({x: self.x_values[i]})
            for i in range(0, degree)
        ]
        slv = sp.solve(linear_system)
        to_add = str(list(slv.keys())[-1])
        slv[sp.Symbol(to_add[0] + str(int(to_add[1]) + 1))] = 0
        polynom = P(degree).subs(slv)

        @np.vectorize
        def subs_poly(value):
            return polynom.subs({x: value}).evalf()

        polynom_points = subs_poly(self.x_values)
        return polynom_points

    def lagrange(self) -> sp.Function:
        n = len(self.x_values)
        x = sp.Symbol("x")
        L = 0
        for i in range(n):
            l = 1
            for j in range(n):
                if j != i:
                    l *= (x - self.x_values[j]) / (self.x_values[i] - self.x_values[j])
            L += self.f_x_values[i] * l
        return L.expand()
