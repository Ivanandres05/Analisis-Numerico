import unittest
import numpy as np

from metodos.biseccion import biseccion
from metodos.falsa_posicion import falsa_posicion
from metodos.punto_fijo import punto_fijo
from metodos.newton import newton_raphson
from metodos.secante import secante

from funciones.definiciones import (
    f_bisection, f_false_position, g_fixed_point, f_newton, df_newton, f_secant
)

def dummy_f(x):
    return x**2 - 4

class TestMetodosNumericos(unittest.TestCase):

    def test_biseccion(self):
        root, _ = biseccion(dummy_f, 0.0, 3.0, 1e-3, 100) # raíz en 2.0
        self.assertLess(abs(dummy_f(root)), 1e-3)

    def test_falsa_posicion(self):
        root, _ = falsa_posicion(dummy_f, 0.0, 3.0, 1e-3, 100)
        self.assertLess(abs(dummy_f(root)), 1e-2)

    def test_punto_fijo(self):
        root, _ = punto_fijo(g_fixed_point, 1.0, 1e-4, 100)
        # La raiz r debe cumplir r = g(r)
        self.assertLess(abs(root - g_fixed_point(root)), 1e-4)

    def test_newton(self):
        root, _ = newton_raphson(f_newton, df_newton, 5.0, 1e-3, 100) # n0=3 da derivada 0
        self.assertLess(abs(f_newton(root)), 1e-3)

    def test_secante(self):
        root, _ = secante(f_secant, 0.5, 1.0, 1e-3, 100)
        self.assertLess(abs(f_secant(root)), 1e-3)

if __name__ == '__main__':
    unittest.main()
