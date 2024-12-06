# -*- coding: utf-8 -*-
"""
Pruebas para las funciones en tasas.py (rendimiento al vencimiento):
"""

import unittest
from bonos.tasas import rendimiento_vencimiento

class TestTasas(unittest.TestCase):
    def test_rendimiento_vencimiento(self):
        # Prueba con un bono de 10 años con pagos anuales
        ytm = rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=10, frecuencia=1)
        self.assertAlmostEqual(ytm, 5.57, places=2)

        # Prueba con un bono de 5 años con pagos semestrales
        ytm = rendimiento_vencimiento(precio_bono=980, valor_nominal=1000, tasa_cupon=4, periodos=5, frecuencia=2)
        self.assertAlmostEqual(ytm, 4.30, places=2)

    def test_rendimiento_vencimiento_exacto(self):
        # Prueba con un bono cuyo precio coincide con el valor nominal (YTM = tasa de cupón)
        ytm = rendimiento_vencimiento(precio_bono=1000, valor_nominal=1000, tasa_cupon=5, periodos=10, frecuencia=1)
        self.assertAlmostEqual(ytm, 5.00, places=2)

    def test_rendimiento_vencimiento_zero_coupon(self):
        # Prueba con un bono cero cupón
        ytm = rendimiento_vencimiento(precio_bono=613.91, valor_nominal=1000, tasa_cupon=0, periodos=10, frecuencia=1)
        self.assertAlmostEqual(ytm, 5.00, places=2)

    def test_invalid_precio_bono(self):
        """
        Verifica que se levante una excepción si el precio del bono no es un número.
        """
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono="950", valor_nominal=1000, tasa_cupon=5, periodos=10, frecuencia=1)

    def test_invalid_valor_nominal(self):
        """
        Verifica que se levante una excepción si el valor nominal no es un número.
        """
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono=950, valor_nominal="1000", tasa_cupon=5, periodos=10, frecuencia=1)

    def test_invalid_tasa_cupon(self):
        """
        Verifica que se levante una excepción si la tasa de cupón no es un número.
        """
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon="5", periodos=10, frecuencia=1)

    def test_invalid_periodos(self):
        """
        Verifica que se levante una excepción si el número de periodos no es un entero positivo.
        """
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=-1, frecuencia=1)
        
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=0, frecuencia=1)
        
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=10.5, frecuencia=1)
        
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos="10", frecuencia=1)

    def test_invalid_frecuencia(self):
        """
        Verifica que se levante una excepción si la frecuencia no es un entero positivo.
        """
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=10, frecuencia=-1)
        
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=10, frecuencia=0)
        
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=10, frecuencia=2.5)
        
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=10, frecuencia="2")

    def test_invalid_guess(self):
        """
        Verifica que se levante una excepción si la suposición inicial (guess) no es un número.
        """
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=10, frecuencia=1, guess="0.05")

    def test_invalid_tol(self):
        """
        Verifica que se levante una excepción si la tolerancia (tol) no es un número positivo.
        """
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=10, frecuencia=1, tol=-1e-6)
        
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=10, frecuencia=1, tol=0)

    def test_invalid_max_iter(self):
        """
        Verifica que se levante una excepción si el número máximo de iteraciones (max_iter) no es un entero positivo.
        """
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=10, frecuencia=1, max_iter=0)
        
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=10, frecuencia=1, max_iter=1000.5)
        
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=10, frecuencia=1, max_iter="1000")

    def test_no_convergencia(self):
        """
        Verifica que se levante una excepción si el método de Newton-Raphson no converge.
        """
        with self.assertRaises(ValueError):
            rendimiento_vencimiento(precio_bono=950, valor_nominal=1000, tasa_cupon=5, periodos=10, frecuencia=1, guess=1.0, tol=1e-6, max_iter=1)

if __name__ == "__main__":
    unittest.main()