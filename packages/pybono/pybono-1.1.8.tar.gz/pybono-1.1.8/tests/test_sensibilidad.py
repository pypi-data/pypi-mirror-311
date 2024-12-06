# -*- coding: utf-8 -*-
"""
Pruebas para las funciones de duración de Macaulay y, si decides implementarla, convexidad.
"""

import unittest
from bonos.sensibilidad import duracion_macaulay  # Importar la función que estamos probando

class TestSensibilidad(unittest.TestCase):

    def setUp(self):
        self.valor_nominal = 1000
        self.tasa_cupon = 5  # 5% anual
        self.tasa_descuento = 3  # 3% anual
        self.periodos = 5  # 5 años
        self.frecuencia = 1  # Pago anual

    def test_duracion_macaulay_anual(self):
        """
        Prueba de la duración de Macaulay para un bono con pagos anuales.
        """
        duracion_esperada = 4.43
        duracion_calculada = duracion_macaulay(self.valor_nominal, self.tasa_cupon, self.tasa_descuento, self.periodos, self.frecuencia)
        self.assertAlmostEqual(duracion_calculada, duracion_esperada, places=2)

    def test_duracion_macaulay_semestral(self):
        """
        Prueba de la duración de Macaulay para un bono con pagos semestrales.
        """
        valor_nominal = 1000
        tasa_cupon = 6  # 6% anual
        tasa_descuento = 4  # 4% anual
        periodos = 10  # 10 años
        frecuencia = 2  # Pago semestral

        duracion_esperada = 8.33
        duracion_calculada = duracion_macaulay(valor_nominal, tasa_cupon, tasa_descuento, periodos, frecuencia)
        self.assertAlmostEqual(duracion_calculada, duracion_esperada, places=2)

    def test_duracion_macaulay_sin_cupones(self):
        """
        Prueba de la duración de Macaulay para un bono sin cupones (bono cero).
        """
        valor_nominal = 1000
        tasa_cupon = 0  # Sin cupones
        tasa_descuento = 5  # 5% anual
        periodos = 10  # 10 años
        frecuencia = 1  # Pago único al vencimiento

        duracion_esperada = 10
        duracion_calculada = duracion_macaulay(valor_nominal, tasa_cupon, tasa_descuento, periodos, frecuencia)
        self.assertAlmostEqual(duracion_calculada, duracion_esperada, places=2)

    def test_invalid_valor_nominal(self):
        """
        Verifica que se levante una excepción si el valor nominal no es un número.
        """
        with self.assertRaises(ValueError):
            duracion_macaulay("1000", self.tasa_cupon, self.tasa_descuento, self.periodos, self.frecuencia)

    def test_invalid_tasa_cupon(self):
        """
        Verifica que se levante una excepción si la tasa de cupón no es un número.
        """
        with self.assertRaises(ValueError):
            duracion_macaulay(self.valor_nominal, "5", self.tasa_descuento, self.periodos, self.frecuencia)

    def test_invalid_tasa_descuento(self):
        """
        Verifica que se levante una excepción si la tasa de descuento no es un número.
        """
        with self.assertRaises(ValueError):
            duracion_macaulay(self.valor_nominal, self.tasa_cupon, "3", self.periodos, self.frecuencia)

    def test_invalid_periodos(self):
        """
        Verifica que se levante una excepción si el número de periodos no es un entero positivo.
        """
        with self.assertRaises(ValueError):
            duracion_macaulay(self.valor_nominal, self.tasa_cupon, self.tasa_descuento, -1, self.frecuencia)
        
        with self.assertRaises(ValueError):
            duracion_macaulay(self.valor_nominal, self.tasa_cupon, self.tasa_descuento, 0, self.frecuencia)
        
        with self.assertRaises(ValueError):
            duracion_macaulay(self.valor_nominal, self.tasa_cupon, self.tasa_descuento, 5.5, self.frecuencia)
        
        with self.assertRaises(ValueError):
            duracion_macaulay(self.valor_nominal, self.tasa_cupon, self.tasa_descuento, "5", self.frecuencia)

    def test_invalid_frecuencia(self):
        """
        Verifica que se levante una excepción si la frecuencia no es un entero positivo.
        """
        with self.assertRaises(ValueError):
            duracion_macaulay(self.valor_nominal, self.tasa_cupon, self.tasa_descuento, self.periodos, -1)
        
        with self.assertRaises(ValueError):
            duracion_macaulay(self.valor_nominal, self.tasa_cupon, self.tasa_descuento, self.periodos, 0)
        
        with self.assertRaises(ValueError):
            duracion_macaulay(self.valor_nominal, self.tasa_cupon, self.tasa_descuento, self.periodos, 2.5)
        
        with self.assertRaises(ValueError):
            duracion_macaulay(self.valor_nominal, self.tasa_cupon, self.tasa_descuento, self.periodos, "2")

    def test_valor_presente_cero(self):
        """
        Verifica que se levante una excepción si el valor presente de los flujos es cero.
        """
        valor_nominal = 1000
        tasa_cupon = 0  # Sin cupones
        tasa_descuento = 0  # Tasa de descuento cero
        periodos = 10  # 10 años
        frecuencia = 1  # Pago único al vencimiento

        with self.assertRaises(ValueError):
            duracion_macaulay(valor_nominal, tasa_cupon, tasa_descuento, periodos, frecuencia)

if __name__ == "__main__":
    unittest.main()