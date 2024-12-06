# -*- coding: utf-8 -*-
"""
Pruebas unitarias para las funciones de visualización que se encuentran en visualizacion.py. Usaremos el módulo unittest.
"""

import unittest
from bonos.visualizacion import graficar_flujos, graficar_tasas_simuladas
import matplotlib.pyplot as plt

class TestVisualizacion(unittest.TestCase):
    def setUp(self):
        # Configuramos datos para las pruebas
        self.flujos = [100, 100, 1100]
        self.plazos = [1, 2, 3]
        self.tasas_simuladas = [0.04, 0.05, 0.06, 0.07, 0.04]

    def test_graficar_flujos(self):
        """
        Prueba de la función graficar_flujos.
        """
        try:
            graficar_flujos(self.flujos, self.plazos)
        except Exception as e:
            self.fail(f"graficar_flujos lanzó una excepción: {e}")

    def test_graficar_flujos_invalid_flujos(self):
        """
        Verifica que se levante una excepción si los flujos no son una lista.
        """
        with self.assertRaises(ValueError):
            graficar_flujos((100, 100, 1100), self.plazos)

    def test_graficar_flujos_flujos_vacio(self):
        """
        Verifica que se levante una excepción si la lista de flujos está vacía.
        """
        with self.assertRaises(ValueError):
            graficar_flujos([], self.plazos)

    def test_graficar_flujos_invalid_plazos(self):
        """
        Verifica que se levante una excepción si los plazos no son una lista.
        """
        with self.assertRaises(ValueError):
            graficar_flujos(self.flujos, (1, 2, 3))

    def test_graficar_flujos_plazos_vacio(self):
        """
        Verifica que se levante una excepción si la lista de plazos está vacía.
        """
        with self.assertRaises(ValueError):
            graficar_flujos(self.flujos, [])

    def test_graficar_flujos_flujos_plazos_longitud_diferente(self):
        """
        Verifica que se levante una excepción si las listas de flujos y plazos no tienen la misma longitud.
        """
        with self.assertRaises(ValueError):
            graficar_flujos(self.flujos, [1, 2])

    def test_graficar_tasas_simuladas(self):
        """
        Prueba de la función graficar_tasas_simuladas.
        """
        try:
            graficar_tasas_simuladas(self.tasas_simuladas)
        except Exception as e:
            self.fail(f"graficar_tasas_simuladas lanzó una excepción: {e}")

    def test_graficar_tasas_simuladas_invalid_tasas(self):
        """
        Verifica que se levante una excepción si las tasas simuladas no son una lista.
        """
        with self.assertRaises(ValueError):
            graficar_tasas_simuladas((0.04, 0.05, 0.06, 0.07, 0.04))

    def test_graficar_tasas_simuladas_tasas_vacia(self):
        """
        Verifica que se levante una excepción si la lista de tasas simuladas está vacía.
        """
        with self.assertRaises(ValueError):
            graficar_tasas_simuladas([])

if __name__ == '__main__':
    unittest.main()