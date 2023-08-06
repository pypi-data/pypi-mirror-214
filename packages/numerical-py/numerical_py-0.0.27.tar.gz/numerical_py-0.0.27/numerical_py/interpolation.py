import numpy as np
import sympy as sp

class Interpolate:

    def __init__(self,x_values: np.ndarray, f_x_values: np.ndarray) -> None:
        self.x_values = x_values
        self.f_x_values = f_x_values

    def lagrange_polynom(self) -> sp.function:
        n = len(self.x_values)
        x = sp.Symbol('x')
        L = 0
        for i in range(n):
            l = 1
            for j in range(n):
                if j != i:
                    l *= (x - self.x_values[j])/(self.x_values[i] - self.x_values[j])
            L += self.f_x_values[i]*l
        return L.expand()
