from typing import Tuple
import numpy as np

class LinearSystemEquations:

    def __init__(self, A: np.ndarray, B: np.ndarray, eps: float, max_iterations: int) -> None:
        self.A = A
        self.B = B
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
        flag, q = self.check_convergence(self.A)
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
        for iter in range(self.max_iter):
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