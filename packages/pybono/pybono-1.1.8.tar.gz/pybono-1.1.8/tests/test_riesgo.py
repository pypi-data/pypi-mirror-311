# -*- coding: utf-8 -*-
"""
Pruebas para las funciones de cálculo de duración y convexidad.
"""

import unittest
from bonos.riesgo import calcular_duracion, calcular_convexidad

class TestRiesgo(unittest.TestCase):
    def setUp(self):
        self.flujos = [100, 100, 1100]  # Flujos de efectivo
        self.tasas = 0.05                # Tasa de descuento (5%)
        self.plazos = [1, 2, 3]          # Plazos en años

    def test_calcular_duracion(self):
        duracion = calcular_duracion(self.flujos, self.tasas, self.plazos)
        self.assertAlmostEqual(duracion, 2.76, places=2)  # Comparando con un valor esperado

    def test_calcular_convexidad(self):
        convexidad = calcular_convexidad(self.flujos, self.tasas, self.plazos)
        self.assertAlmostEqual(convexidad, 8.25, places=2)  # Comparando con un valor esperado

    def test_flujos_no_lista(self):
        """
        Verifica que se levante una excepción si los flujos no son una lista.
        """
        with self.assertRaises(ValueError):
            calcular_duracion((100, 100, 1100), self.tasas, self.plazos)

    def test_tasa_no_numero(self):
        """
        Verifica que se levante una excepción si la tasa de descuento no es un número.
        """
        with self.assertRaises(ValueError):
            calcular_duracion(self.flujos, "0.05", self.plazos)

    def test_plazos_no_lista(self):
        """
        Verifica que se levante una excepción si los plazos no son una lista.
        """
        with self.assertRaises(ValueError):
            calcular_duracion(self.flujos, self.tasas, (1, 2, 3))

    def test_flujos_plazos_longitud_diferente(self):
        """
        Verifica que se levante una excepción si las listas de flujos y plazos no tienen la misma longitud.
        """
        with self.assertRaises(ValueError):
            calcular_duracion(self.flujos, self.tasas, [1, 2])

    def test_flujos_vacia(self):
        """
        Verifica que se levante una excepción si la lista de flujos está vacía.
        """
        with self.assertRaises(ValueError):
            calcular_duracion([], self.tasas, self.plazos)

    def test_plazos_vacia(self):
        """
        Verifica que se levante una excepción si la lista de plazos está vacía.
        """
        with self.assertRaises(ValueError):
            calcular_duracion(self.flujos, self.tasas, [])

    def test_valor_presente_cero(self):
        """
        Verifica que se levante una excepción si el valor presente de los flujos es cero.
        """
        flujos_cero = [0, 0, 0]
        with self.assertRaises(ValueError):
            calcular_duracion(flujos_cero, self.tasas, self.plazos)

    def test_convexidad_flujos_no_lista(self):
        """
        Verifica que se levante una excepción si los flujos no son una lista para calcular convexidad.
        """
        with self.assertRaises(ValueError):
            calcular_convexidad((100, 100, 1100), self.tasas, self.plazos)

    def test_convexidad_tasa_no_numero(self):
        """
        Verifica que se levante una excepción si la tasa de descuento no es un número para calcular convexidad.
        """
        with self.assertRaises(ValueError):
            calcular_convexidad(self.flujos, "0.05", self.plazos)

    def test_convexidad_plazos_no_lista(self):
        """
        Verifica que se levante una excepción si los plazos no son una lista para calcular convexidad.
        """
        with self.assertRaises(ValueError):
            calcular_convexidad(self.flujos, self.tasas, (1, 2, 3))

    def test_convexidad_flujos_plazos_longitud_diferente(self):
        """
        Verifica que se levante una excepción si las listas de flujos y plazos no tienen la misma longitud para calcular convexidad.
        """
        with self.assertRaises(ValueError):
            calcular_convexidad(self.flujos, self.tasas, [1, 2])

    def test_convexidad_flujos_vacia(self):
        """
        Verifica que se levante una excepción si la lista de flujos está vacía para calcular convexidad.
        """
        with self.assertRaises(ValueError):
            calcular_convexidad([], self.tasas, self.plazos)

    def test_convexidad_plazos_vacia(self):
        """
        Verifica que se levante una excepción si la lista de plazos está vacía para calcular convexidad.
        """
        with self.assertRaises(ValueError):
            calcular_convexidad(self.flujos, self.tasas, [])

    def test_convexidad_valor_presente_cero(self):
        """
        Verifica que se levante una excepción si el valor presente de los flujos es cero para calcular convexidad.
        """
        flujos_cero = [0, 0, 0]
        with self.assertRaises(ValueError):
            calcular_convexidad(flujos_cero, self.tasas, self.plazos)

    def test_duracion_y_convexidad_con_tasa_cero(self):
        """
        Verifica que la duración y convexidad sean correctas cuando la tasa de descuento es cero.
        """
        tasa_cero = 0.0
        duracion = calcular_duracion(self.flujos, tasa_cero, self.plazos)
        convexidad = calcular_convexidad(self.flujos, tasa_cero, self.plazos)
        self.assertAlmostEqual(duracion, 2.33, places=2)  # Valor esperado para tasa = 0
        self.assertAlmostEqual(convexidad, 8.00, places=2)  # Valor esperado para tasa = 0

    def test_duracion_y_convexidad_con_tasa_alta(self):
        """
        Verifica que la duración y convexidad sean correctas cuando la tasa de descuento es alta.
        """
        tasa_alta = 0.20
        duracion = calcular_duracion(self.flujos, tasa_alta, self.plazos)
        convexidad = calcular_convexidad(self.flujos, tasa_alta, self.plazos)
        self.assertAlmostEqual(duracion, 1.91, places=2)  # Valor esperado para tasa = 0.20
        self.assertAlmostEqual(convexidad, 3.33, places=2)  # Valor esperado para tasa = 0.20

if __name__ == '__main__':
    unittest.main()