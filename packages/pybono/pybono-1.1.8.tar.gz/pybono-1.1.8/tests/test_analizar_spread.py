# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 23:44:59 2024

@author: Luis Humberto Calderon Baldeón
"""

import unittest
from bonos.credito import analizar_spread

class TestAnalizarSpread(unittest.TestCase):

    def setUp(self):
        # Configuración de un bono corporativo y un bono gubernamental de prueba
        self.bono_corporativo = {
            "precio": 950,           # Precio actual del bono corporativo
            "valor_nominal": 1000,   # Valor nominal del bono corporativo
            "tasa_cupon": 0.06,      # Tasa de cupón (6%)
            "periodos": 10           # Periodos hasta el vencimiento
        }
        self.bono_gubernamental = {
            "precio": 980,           # Precio actual del bono gubernamental
            "valor_nominal": 1000,   # Valor nominal del bono gubernamental
            "tasa_cupon": 0.04,      # Tasa de cupón (4%)
            "periodos": 10           # Periodos hasta el vencimiento
        }
        # Tasas de descuento para evaluar el spread
        self.tasas_descuento = [0.03, 0.04, 0.05]

    def test_calculo_spread(self):
        """
        Verifica que el cálculo de spreads sea correcto para una lista de tasas de descuento.
        """
        resultados = analizar_spread(
            bono_corporativo=self.bono_corporativo,
            bono_gubernamental=self.bono_gubernamental,
            tasas_descuento=self.tasas_descuento
        )

        # Verificar que los spreads se calculan para todas las tasas de descuento
        self.assertEqual(len(resultados["spreads"]), len(self.tasas_descuento))

        # Verificar que el spread promedio, mínimo y máximo sean consistentes
        self.assertAlmostEqual(resultados["promedio"], sum(resultados["spreads"]) / len(resultados["spreads"]), places=5)
        self.assertEqual(resultados["minimo"], min(resultados["spreads"]))
        self.assertEqual(resultados["maximo"], max(resultados["spreads"]))

    def test_spread_positivo(self):
        """
        Verifica que los spreads sean positivos si el rendimiento corporativo es mayor al gubernamental.
        """
        resultados = analizar_spread(
            bono_corporativo=self.bono_corporativo,
            bono_gubernamental=self.bono_gubernamental,
            tasas_descuento=self.tasas_descuento
        )

        # Verificar que todos los spreads sean positivos
        for spread in resultados["spreads"]:
            self.assertGreaterEqual(spread, 0)

    def test_spread_cero(self):
        """
        Verifica el caso en que los bonos tienen rendimientos iguales (spread = 0).
        """
        # Modificar el bono corporativo para que tenga el mismo rendimiento que el gubernamental
        bono_corporativo_igual = {
            "precio": 980,           # Mismo precio
            "valor_nominal": 1000,   # Mismo valor nominal
            "tasa_cupon": 0.04,      # Misma tasa de cupón
            "periodos": 10           # Mismo número de periodos
        }

        resultados = analizar_spread(
            bono_corporativo=bono_corporativo_igual,
            bono_gubernamental=self.bono_gubernamental,
            tasas_descuento=self.tasas_descuento
        )

        # Verificar que todos los spreads sean 0
        for spread in resultados["spreads"]:
            self.assertAlmostEqual(spread, 0, places=5)

    def test_spread_negativo(self):
        """
        Verifica el caso en que el rendimiento del bono gubernamental es mayor al corporativo.
        """
        # Modificar el bono gubernamental para que tenga mayor rendimiento
        bono_gubernamental_mayor = {
            "precio": 900,           # Precio más bajo
            "valor_nominal": 1000,   # Mismo valor nominal
            "tasa_cupon": 0.07,      # Mayor tasa de cupón
            "periodos": 10           # Mismo número de periodos
        }

        resultados = analizar_spread(
            bono_corporativo=self.bono_corporativo,
            bono_gubernamental=bono_gubernamental_mayor,
            tasas_descuento=self.tasas_descuento
        )

        # Verificar que todos los spreads sean negativos
        for spread in resultados["spreads"]:
            self.assertLessEqual(spread, 0)

    def test_invalid_bono_corporativo(self):
        """
        Verifica que se levante una excepción si el bono corporativo no tiene las claves necesarias.
        """
        bono_corporativo_invalido = {
            "precio": 950,
            "valor_nominal": 1000,
            "tasa_cupon": 0.06
            # Falta "periodos"
        }

        with self.assertRaises(KeyError):
            analizar_spread(
                bono_corporativo=bono_corporativo_invalido,
                bono_gubernamental=self.bono_gubernamental,
                tasas_descuento=self.tasas_descuento
            )

    def test_invalid_bono_gubernamental(self):
        """
        Verifica que se levante una excepción si el bono gubernamental no tiene las claves necesarias.
        """
        bono_gubernamental_invalido = {
            "precio": 980,
            "valor_nominal": 1000,
            "tasa_cupon": 0.04
            # Falta "periodos"
        }

        with self.assertRaises(KeyError):
            analizar_spread(
                bono_corporativo=self.bono_corporativo,
                bono_gubernamental=bono_gubernamental_invalido,
                tasas_descuento=self.tasas_descuento
            )

    def test_invalid_tasas_descuento(self):
        """
        Verifica que se levante una excepción si las tasas de descuento no son una lista de números.
        """
        tasas_descuento_invalidas = [0.03, "0.04", 0.05]

        with self.assertRaises(ValueError):
            analizar_spread(
                bono_corporativo=self.bono_corporativo,
                bono_gubernamental=self.bono_gubernamental,
                tasas_descuento=tasas_descuento_invalidas
            )

if __name__ == '__main__':
    unittest.main()