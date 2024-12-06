# -*- coding: utf-8 -*-
"""
Pruebas unitarias para las funciones de cálculo del precio de un bono que se encuentran en valuacion.py. Usaremos el módulo unittest.
"""

import unittest
from bonos.valuacion import precio_bono

class TestValuacion(unittest.TestCase):
    def test_precio_bono_anual(self):
        """
        Prueba del precio de un bono con pagos anuales.
        """
        valor_nominal = 1000
        tasa_cupon = 5  # 5% anual
        tasa_descuento = 3  # 3% anual
        periodos = 5  # 5 años
        frecuencia = 1  # Pago anual

        # El precio esperado se calcula de forma teórica
        precio_esperado = 1086.07
        precio_calculado = precio_bono(valor_nominal, tasa_cupon, tasa_descuento, periodos, frecuencia)

        self.assertAlmostEqual(precio_calculado, precio_esperado, places=2)

    def test_precio_bono_semestral(self):
        """
        Prueba del precio de un bono con pagos semestrales.
        """
        valor_nominal = 1000
        tasa_cupon = 6  # 6% anual
        tasa_descuento = 4  # 4% anual
        periodos = 10  # 10 años
        frecuencia = 2  # Pago semestral

        # El precio esperado se calcula de forma teórica
        precio_esperado = 1104.26
        precio_calculado = precio_bono(valor_nominal, tasa_cupon, tasa_descuento, periodos, frecuencia)

        self.assertAlmostEqual(precio_calculado, precio_esperado, places=2)

    def test_precio_bono_cero(self):
        """
        Prueba del precio de un bono cero cupón.
        """
        valor_nominal = 1000
        tasa_cupon = 0  # Sin cupones
        tasa_descuento = 5  # 5% anual
        periodos = 5  # 5 años
        frecuencia = 1  # Pago único al vencimiento

        # El precio esperado se calcula de forma teórica
        precio_esperado = 783.53
        precio_calculado = precio_bono(valor_nominal, tasa_cupon, tasa_descuento, periodos, frecuencia)

        self.assertAlmostEqual(precio_calculado, precio_esperado, places=2)

    def test_invalid_valor_nominal(self):
        """
        Verifica que se levante una excepción si el valor nominal no es un número.
        """
        with self.assertRaises(ValueError):
            precio_bono(valor_nominal="1000", tasa_cupon=5, tasa_descuento=3, periodos=5, frecuencia=1)

    def test_invalid_tasa_cupon(self):
        """
        Verifica que se levante una excepción si la tasa de cupón no es un número.
        """
        with self.assertRaises(ValueError):
            precio_bono(valor_nominal=1000, tasa_cupon="5", tasa_descuento=3, periodos=5, frecuencia=1)

    def test_invalid_tasa_descuento(self):
        """
        Verifica que se levante una excepción si la tasa de descuento no es un número.
        """
        with self.assertRaises(ValueError):
            precio_bono(valor_nominal=1000, tasa_cupon=5, tasa_descuento="3", periodos=5, frecuencia=1)

    def test_invalid_periodos(self):
        """
        Verifica que se levante una excepción si el número de periodos no es un entero positivo.
        """
        with self.assertRaises(ValueError):
            precio_bono(valor_nominal=1000, tasa_cupon=5, tasa_descuento=3, periodos=-1, frecuencia=1)
        
        with self.assertRaises(ValueError):
            precio_bono(valor_nominal=1000, tasa_cupon=5, tasa_descuento=3, periodos=0, frecuencia=1)
        
        with self.assertRaises(ValueError):
            precio_bono(valor_nominal=1000, tasa_cupon=5, tasa_descuento=3, periodos=5.5, frecuencia=1)
        
        with self.assertRaises(ValueError):
            precio_bono(valor_nominal=1000, tasa_cupon=5, tasa_descuento=3, periodos="5", frecuencia=1)

    def test_invalid_frecuencia(self):
        """
        Verifica que se levante una excepción si la frecuencia no es un entero positivo.
        """
        with self.assertRaises(ValueError):
            precio_bono(valor_nominal=1000, tasa_cupon=5, tasa_descuento=3, periodos=5, frecuencia=-1)
        
        with self.assertRaises(ValueError):
            precio_bono(valor_nominal=1000, tasa_cupon=5, tasa_descuento=3, periodos=5, frecuencia=0)
        
        with self.assertRaises(ValueError):
            precio_bono(valor_nominal=1000, tasa_cupon=5, tasa_descuento=3, periodos=5, frecuencia=2.5)
        
        with self.assertRaises(ValueError):
            precio_bono(valor_nominal=1000, tasa_cupon=5, tasa_descuento=3, periodos=5, frecuencia="2")

    def test_precio_bono_trimestral(self):
        """
        Prueba del precio de un bono con pagos trimestrales.
        """
        valor_nominal = 1000
        tasa_cupon = 8  # 8% anual
        tasa_descuento = 5  # 5% anual
        periodos = 4  # 4 años
        frecuencia = 4  # Pago trimestral

        # El precio esperado se calcula de forma teórica
        precio_esperado = 1062.54
        precio_calculado = precio_bono(valor_nominal, tasa_cupon, tasa_descuento, periodos, frecuencia)

        self.assertAlmostEqual(precio_calculado, precio_esperado, places=2)

    def test_precio_bono_mensual(self):
        """
        Prueba del precio de un bono con pagos mensuales.
        """
        valor_nominal = 1000
        tasa_cupon = 10  # 10% anual
        tasa_descuento = 6  # 6% anual
        periodos = 3  # 3 años
        frecuencia = 12  # Pago mensual

        # El precio esperado se calcula de forma teórica
        precio_esperado = 1056.75
        precio_calculado = precio_bono(valor_nominal, tasa_cupon, tasa_descuento, periodos, frecuencia)

        self.assertAlmostEqual(precio_calculado, precio_esperado, places=2)

if __name__ == "__main__":
    unittest.main()