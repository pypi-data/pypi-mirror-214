import numpy as np
import sympy as sp

def direct_deployment_method(matrix: sp.Matrix):
    lam = sp.symbols('lam')
    n = matrix.shape[0]
    E = np.eye(n)
    det = sp.det(matrix - lam * E)
    roots = sp.solve(det, lam)
    return roots