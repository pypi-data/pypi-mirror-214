import numpy as np
import sympy as sp

class Eigenvals:

    def __init__(self, matrix: sp.Matrix) -> None:
        self.matrix = matrix

    def direct_deployment_method(self):
        lam = sp.symbols('lam')
        n = self.matrix.shape[0]
        E = np.eye(n)
        det = sp.det(self.matrix - lam * E)
        lambda_ = sp.solve(det, lam)
        eigen = {"roots": lambda_}

        eigenitems = []

        for l in lambda_:
            print(f"λ = {l:.2f} is an eigenvalue of A")
            x = sp.Matrix(sp.symbols(f"x:{self.matrix.shape[0]}"))
            sol = sp.solve((self.matrix - l * sp.eye(self.matrix.shape[0])) * x, x)
            print(f"eigenvector: {sol}\n")
            eigenitems.append({"value": l, "vector": sol})

        eigen["items"] = eigenitems

        return eigen
    
    def iteration_method(self, x0: np.matrix, eps: float):
        x = self.matrix @ x0
        lambda_ = x[0, 0] / x0[0, 0]
        k = 1
        while True:
            x_new = self.matrix @ x
            lambda_new = x_new[0, 0] / x[0, 0]
            print(f"iteration {k}: λ = {lambda_new:.4f}")
            if abs(lambda_new - lambda_) < eps:
                break

            lambda_ = lambda_new
            x = x_new
            k += 1

        return lambda_new, x / x[0, 0]
