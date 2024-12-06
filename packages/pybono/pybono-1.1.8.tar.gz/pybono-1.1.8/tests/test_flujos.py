# -*- coding: utf-8 -*-
"""
Pruebas unitarias para la generación de flujos de caja de bonos.
"""

import unittest
from bonos.flujos import generar_flujos

class TestFlujos(unittest.TestCase):

    def test_flujos_anuales(self):
        """
        Prueba de generación de flujos de caja para un bono con pagos anuales.
        """
        valor_nominal = 1000
        tasa_cupon = 5  # 5% anual
        periodos = 5  # 5 años
        frecuencia = 1  # Pagos anuales

        # Flujos esperados: 50 cada año durante 5 años, con 1000 al final
        flujos_esperados = [50.0, 50.0, 50.0, 50.0, 1050.0]
        flujos_generados = generar_flujos(valor_nominal, tasa_cupon, periodos, frecuencia)

        self.assertEqual(flujos_generados, flujos_esperados)

    def test_flujos_semestrales(self):
        """
        Prueba de generación de flujos de caja para un bono con pagos semestrales.
        """
        valor_nominal = 1000
        tasa_cupon = 6  # 6% anual
        periodos = 3  # 3 años
        frecuencia = 2  # Pagos semestrales

        # Flujos esperados: 30 cada semestre durante 6 semestres, con 1000 al final
        flujos_esperados = [30.0, 30.0, 30.0, 30.0, 30.0, 1030.0]
        flujos_generados = generar_flujos(valor_nominal, tasa_cupon, periodos, frecuencia)

        self.assertEqual(flujos_generados, flujos_esperados)

    def test_flujos_trimestrales(self):
        """
        Prueba de generación de flujos de caja para un bono con pagos trimestrales.
        """
        valor_nominal = 2000
        tasa_cupon = 4  # 4% anual
        periodos = 2  # 2 años
        frecuencia = 4  # Pagos trimestrales

        # Flujos esperados: 20 cada trimestre durante 8 trimestres, con 2000 al final
        flujos_esperados = [20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 2020.0]
        flujos_generados = generar_flujos(valor_nominal, tasa_cupon, periodos, frecuencia)

        self.assertEqual(flujos_generados, flujos_esperados)

    def test_flujos_frecuencia_irregular(self):
        """
        Prueba de generación de flujos de caja para un bono con una frecuencia irregular (3 pagos al año).
        """
        valor_nominal = 1500
        tasa_cupon = 9  # 9% anual
        periodos = 4  # 4 años
        frecuencia = 3  # 3 pagos al año

        # Flujos esperados: 45 cada periodo durante 12 periodos, con 1500 al final
        flujos_esperados = [45.0] * 11 + [1545.0]
        flujos_generados = generar_flujos(valor_nominal, tasa_cupon, periodos, frecuencia)

        self.assertEqual(flujos_generados, flujos_esperados)

    def test_flujos_sin_cupones(self):
        """
        Prueba de generación de flujos de caja para un bono sin cupones (bono 'cero').
        """
        valor_nominal = 1000
        tasa_cupon = 0  # Sin cupones
        periodos = 10  # 10 años
        frecuencia = 1  # Pago único al vencimiento

        # Flujos esperados: Solo un pago al final
        flujos_esperados = [0.0] * 9 + [1000.0]
        flujos_generados = generar_flujos(valor_nominal, tasa_cupon, periodos, frecuencia)

        self.assertEqual(flujos_generados, flujos_esperados)

    def test_invalid_valor_nominal(self):
        """
        Verifica que se levante una excepción si el valor nominal no es un número.
        """
        with self.assertRaises(ValueError):
            generar_flujos("1000", 5, 5, 1)

    def test_invalid_tasa_cupon(self):
        """
        Verifica que se levante una excepción si la tasa de cupón no es un número.
        """
        with self.assertRaises(ValueError):
            generar_flujos(1000, "5", 5, 1)

    def test_invalid_periodos(self):
        """
        Verifica que se levante una excepción si el número de periodos no es un entero positivo.
        """
        with self.assertRaises(ValueError):
            generar_flujos(1000, 5, -1, 1)
        
        with self.assertRaises(ValueError):
            generar_flujos(1000, 5, 0, 1)
        
        with self.assertRaises(ValueError):
            generar_flujos(1000, 5, 5.5, 1)
        
        with self.assertRaises(ValueError):
            generar_flujos(1000, 5, "5", 1)

    def test_invalid_frecuencia(self):
        """
        Verifica que se levante una excepción si la frecuencia no es un entero positivo.
        """
        with self.assertRaises(ValueError):
            generar_flujos(1000, 5, 5, -1)
        
        with self.assertRaises(ValueError):
            generar_flujos(1000, 5, 5, 0)
        
        with self.assertRaises(ValueError):
            generar_flujos(1000, 5, 5, 5.5)
        
        with self.assertRaises(ValueError):
            generar_flujos(1000, 5, 5, "2")

if __name__ == "__main__":
    unittest.main()