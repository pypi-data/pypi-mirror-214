from typing import Tuple
import numpy as np
import sympy as sp


class LinearSystemEquations:
    def __init__(
        self, A: np.ndarray, B: np.ndarray, eps: float, max_iterations: int
    ) -> None:
        self.A = A.astype('float64')
        self.B = B.astype('float64')
        self.eps = eps
        self.max_iterations = max_iterations

    @staticmethod
    def check_convergence(matrix: np.ndarray) -> Tuple[bool, float]:
        n = len(matrix)
        q = 0
        for i in range(n):
            c_max = 0
            for j in range(n):
                if i != j:
                    c_max += matrix[i][j]
            c_max = c_max / matrix[i][i]
            q = max(q, c_max)

        return (True if q < 1 else False, q)

    def simple_iteration(self) -> Tuple[np.ndarray, int]:
        flag, q = LinearSystemEquations.check_convergence(self.A)
        if not flag:
            print("The method does not converge")
            return None
        n = len(self.A)
        x = np.zeros(n)
        for iter in range(self.max_iterations):
            x_new = np.zeros(n)
            for i in range(n):
                x_new[i] = self.B[i]
                for j in range(n):
                    if i != j:
                        x_new[i] -= self.A[i, j] * x[j]
                x_new[i] /= self.A[i, i]
            if np.max(np.abs(x_new - x)) * q / (1 - q) < self.eps:
                break
            x = x_new
        return x_new, iter

    def seidel_method(self) -> Tuple[np.ndarray, int]:
        flag, q = self.check_convergence(self.A)
        if not flag:
            print("The method does not converge")
            return None
        n = len(self.A)
        x_new = np.zeros(n)
        for iter in range(self.max_iterations):
            abs_delta_x = []
            for i in range(n):
                x_last = x_new[i]
                x_new[i] = self.B[i]
                for j in range(n):
                    if i != j:
                        x_new[i] -= self.A[i, j] * x_new[j]
                x_new[i] /= self.A[i, i]
                abs_delta_x.append(abs(x_new[i] - x_last))
            if max(abs_delta_x) * q / (1 - q) < self.eps:
                break
        return x_new, iter

    def gauss_method(self) -> np.ndarray:
        n = len(self.A)
        for i in range(n):
            for j in range(i + 1, n):
                m = self.A[j, i] / self.A[i, i]
                for k in range(i, n):
                    self.A[j, k] -= m * self.A[i, k]
                self.B[j] -= m * self.B[i]
        x = np.zeros(n)
        for i in range(n - 1, -1, -1):
            x[i] = self.B[i]
            for j in range(i + 1, n):
                x[i] -= self.A[i, j] * x[j]
            x[i] /= self.A[i, i]
        return x


class NonLinearSystemEquations:
    def __init__(
        self,
        f1: sp.Function,
        f2: sp.Function,
        eps: float,
        max_iterations: int,
        x_0: float,
        y_0: float,
    ) -> None:
        self.f1 = f1
        self.f2 = f2
        self.x_0 = x_0
        self.y_0 = y_0
        self.eps = eps
        self.max_iterations = max_iterations

    @staticmethod
    def check_convergence(
        f1: sp.Function, f2: sp.Function, x_0: float, y_0: float
    ) -> Tuple[Tuple[bool, float], Tuple[bool, float]]:
        x, y = sp.symbols("x y")
        q1 = (abs(f1.diff(x)) + abs(f2.diff(x))).subs(x, x_0)
        q2 = (abs(f1.diff(y)) + abs(f2.diff(y))).subs(y, y_0)
        return ((q1 < 1, q1), (q2 < 0, q2))

    def seidel_method(self) -> Tuple[float, float]:
        x, y = sp.symbols("x y")
        item_1, item_2 = NonLinearSystemEquations.check_convergence(
            self.f1, self.f2, self.x_0, self.y_0
        )
        if bool(item_1[0]) + bool(item_2[0]) != 2:
            print("The method does not converge")
            return None
        x_new = self.x_0
        y_new = self.y_0
        Q = max(item_1[1], item_2[1])
        while True:
            x_old = x_new
            y_old = y_new
            x_new = sp.N(self.f1.subs(y, y_old))
            y_new = sp.N(self.f2.subs(x, x_new))
            if (
                Q / (1 - Q) * abs(x_new - x_old) < self.eps
                and Q / (1 - Q) * abs(y_new - y_old) < self.eps
            ):
                break
        return x_new, y_new
