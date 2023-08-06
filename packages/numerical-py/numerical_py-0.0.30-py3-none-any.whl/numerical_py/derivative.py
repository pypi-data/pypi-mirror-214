import numpy as np
import sympy as sp

from interpolation import Interpolate


class Derivative:
    def __init__(
        self, x_values: np.ndarray, f_x_values: np.ndarray, h_val: float = 0.02
    ) -> None:
        self.x_values = x_values
        self.f_x_values = f_x_values
        self.h_val = h_val

    def deriv_by_nodes(self, num_nodes: int = 4) -> float:
        def sub_q(L):
            x = sp.Symbol("x")
            x0 = sp.Symbol("x0")
            x_nodes = sp.symbols(" ".join([f"x{i}" for i in range(1, num_nodes)]))
            h, q = sp.symbols("h q")
            subs_dict = {
                k: v for k, v in zip(x_nodes, [x0 + i * h for i in range(1, num_nodes)])
            }
            subs_dict[x] = x0 + h * q
            return L.subs(subs_dict)

        q = sp.Symbol("q")
        h = sp.Symbol("h")
        x0 = sp.Symbol("x0")
        L = Interpolate(self.x_values, self.f_x_values).lagrange_polynom()
        Ldiff = 1 / h * sub_q(L).diff(q)
        Ldiff2 = 1 / h * Ldiff.diff(q)
        return {
            "first_deriv": [
                Ldiff.subs({x0: self.x_values[0], h: self.h_val, q: i})
                for i in range(len(self.f_x_values))
            ],
            "second_deriv": [
                Ldiff2.subs({x0: self.x_values[0], h: self.h_val, q: i})
                for i in range(len(self.f_x_values))
            ],
        }
