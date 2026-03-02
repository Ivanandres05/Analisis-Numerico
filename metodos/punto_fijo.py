import numpy as np

def punto_fijo(g, x0, tol=1e-8, max_iter=100):
    iterations = []
    
    dg_approx = abs((g(x0 + 1e-5) - g(x0)) / 1e-5)
    if dg_approx >= 1:
        raise ValueError("Condicion de convergencia no satisfecha: |g'(x0)| >= 1.")
        
    xn = x0
    for n in range(1, max_iter + 1):
        x_next = g(xn)
        err_abs = abs(x_next - xn)
        err_rel = float('inf') if x_next == 0 else (err_abs / abs(x_next)) * 100
        
        iterations.append({
            'n': n, 'x_n': xn, 'g(x_n)': x_next, '|x_n - g(x_n)|': err_abs,
            'error_abs': err_abs, 'error_rel': err_rel
        })
        
        if err_abs < tol:
            return x_next, iterations
            
        if np.isinf(x_next) or np.isnan(x_next) or err_abs > 1e10:
             raise ValueError("El método divergió. Condiciones de convergencia no satisfechas.")
             
        xn = x_next
        
    raise RuntimeError("No convergencia (máximo de iteraciones alcanzado)")
