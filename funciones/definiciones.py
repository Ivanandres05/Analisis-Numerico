import numpy as np

# Ejercicio 1
def f_bisection(lam):
    return 2.5 + 0.8 * lam**2 - 3.2 * lam + np.log(lam + 1)

# Ejercicio 2
def f_false_position(x):
    return x**3 - 6*x**2 + 11*x - 6.5

# Ejercicio 3
def g_fixed_point(x):
    return 0.5 * np.cos(x) + 1.5

def f_fixed_point(x):
    return x - g_fixed_point(x)

def dg_fixed_point(x):
    return -0.5 * np.sin(x)

# Ejercicio 4
def f_newton(n):
    return n**3 - 8*n**2 + 20*n - 16

def df_newton(n):
    return 3*n**2 - 16*n + 20

# Ejercicio 5
def f_secant(x):
    return x * np.exp(-x/2) - 0.3

def df_secant_for_newton(x):
    return np.exp(-x/2) * (1 - x/2)
