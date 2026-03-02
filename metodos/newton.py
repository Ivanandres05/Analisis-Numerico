import numpy as np
from typing import Callable, List, Dict

def newton_raphson(f: Callable, df: Callable, x0: float, tol: float=1e-10, max_iter: int=100):
    iterations = []
    xn = x0
    for n in range(1, max_iter + 1):
        fxn = f(xn)
        dfxn = df(xn)
        
        if dfxn == 0:
            raise ZeroDivisionError("División por cero: la derivada de la función es nula.")
            
        x_next = xn - fxn / dfxn
        err_abs = abs(x_next - xn)
        err_rel = float('inf') if x_next == 0 else (err_abs / abs(x_next)) * 100
        
        iterations.append({
            'n': n, 'x_n': xn, 'f(x_n)': fxn, "f'(x_n)": dfxn,
            'error_abs': err_abs, 'error_rel': err_rel
        })
        
        if err_abs < tol or abs(fxn) < tol:
            return x_next, iterations
            
        xn = x_next
        
    raise RuntimeError("No convergencia (máximo de iteraciones alcanzado)")
