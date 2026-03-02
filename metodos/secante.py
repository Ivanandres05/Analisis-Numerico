import numpy as np

def secante(f, x0, x1, tol=1e-9, max_iter=100):
    iterations = []
    xn_prev = x0
    xn = x1
    for n in range(1, max_iter + 1):
        fxn_prev = f(xn_prev)
        fxn = f(xn)
        
        if fxn - fxn_prev == 0:
            raise ZeroDivisionError("División por cero: f(x_n) - f(x_{n-1}) = 0.")
            
        x_next = xn - fxn * (xn - xn_prev) / (fxn - fxn_prev)
        err_abs = abs(x_next - xn)
        err_rel = float('inf') if x_next == 0 else (err_abs / abs(x_next)) * 100
        
        iterations.append({
            'n': n, 'x_{n-1}': xn_prev, 'x_n': xn, 'f(x_{n-1})': fxn_prev,
            'f(x_n)': fxn, 'x_{n+1}': x_next, 'error_abs': err_abs, 'error_rel': err_rel
        })
        
        if err_abs < tol or abs(f(x_next)) < tol:
            return x_next, iterations
            
        xn_prev = xn
        xn = x_next
        
    raise RuntimeError("No convergencia (máximo de iteraciones alcanzado)")
