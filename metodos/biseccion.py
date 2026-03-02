import numpy as np
from typing import Callable, List, Dict

def biseccion(f: Callable, a: float, b: float, tol: float = 1e-6, max_iter: int = 100):
    """Algoritmo de búsqueda de raíces por Bisección."""
    iterations: List[Dict] = []
    fa = f(a)
    fb = f(b)
    
    if fa * fb > 0:
        raise ValueError("Intervalos que no contienen raíz (f(a) y f(b) deben tener signos opuestos).")
        
    c = a
    for n in range(1, max_iter + 1):
        c_prev = c
        c = (a + b) / 2
        fc = f(c)
        
        err_abs = float('inf') if n == 1 else abs(c - c_prev)
        err_rel = float('inf') if (n == 1 or c == 0) else (err_abs / abs(c)) * 100
        
        iterations.append({
            'n': n, 'a': a, 'b': b, 'c': c, 'f(c)': fc, 
            'error_abs': err_abs, 'error_rel': err_rel
        })
        
        if abs(fc) < tol or (n > 1 and err_abs < tol):
            return c, iterations
            
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
            
    raise RuntimeError("No convergencia (máximo de iteraciones alcanzado).")
