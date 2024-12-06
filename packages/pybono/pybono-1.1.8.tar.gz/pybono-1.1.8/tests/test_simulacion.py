# -*- coding: utf-8 -*-
"""
Pruebas para las funciones de simulación de tasas y flujos.
"""

import unittest
import numpy as np
from bonos.simulacion import simular_tasas_inflacion, simular_flujos_bono

class TestSimulacion(unittest.TestCase):
    def setUp(self):
        self.base_tasa = 0.05
        self.desviacion = 0.01
        self.num_escenarios = 1000
        self.flujos = [100, 100, 1100]
        self.plazos = [1, 2, 3]
        self.tasas_simuladas = np.array([0.04, 0.05, 0.06])

    def test_simular_tasas_inflacion(self):
        """
        Prueba de simulación de tasas de inflación.
        """
        tasas_simuladas = simular_tasas_inflacion(base_tasa=self.base_tasa, desviacion=self.desviacion, num_escenarios=self.num_escenarios)
        self.assertEqual(len(tasas_simuladas), self.num_escenarios)  # Asegura que se generan 1000 escenarios
        self.assertAlmostEqual(np.mean(tasas_simuladas), self.base_tasa, delta=0.01)  # Promedio cerca de la tasa base

    def test_simular_flujos_bono(self):
        """
        Prueba de simulación de flujos de bono.
        """
        escenarios = simular_flujos_bono(flujos_originales=self.flujos, tasas_simuladas=self.tasas_simuladas, plazos=self.plazos)
        self.assertEqual(len(escenarios), len(self.tasas_simuladas))  # Tres escenarios generados
        self.assertAlmostEqual(escenarios[0][2], 937.87, places=2)  # Valor presente del flujo final bajo 4%
        self.assertAlmostEqual(escenarios[1][2], 961.17, places=2)  # Valor presente del flujo final bajo 5%
        self.assertAlmostEqual(escenarios[2][2], 985.07, places=2)  # Valor presente del flujo final bajo 6%

    def test_simular_tasas_inflacion_invalid_base_tasa(self):
        """
        Verifica que se levante una excepción si la tasa base no es un número.
        """
        with self.assertRaises(ValueError):
            simular_tasas_inflacion(base_tasa="0.05", desviacion=self.desviacion, num_escenarios=self.num_escenarios)

    def test_simular_tasas_inflacion_invalid_desviacion(self):
        """
        Verifica que se levante una excepción si la desviación no es un número.
        """
        with self.assertRaises(ValueError):
            simular_tasas_inflacion(base_tasa=self.base_tasa, desviacion="0.01", num_escenarios=self.num_escenarios)

    def test_simular_tasas_inflacion_invalid_num_escenarios(self):
        """
        Verifica que se levante una excepción si el número de escenarios no es un entero positivo.
        """
        with self.assertRaises(ValueError):
            simular_tasas_inflacion(base_tasa=self.base_tasa, desviacion=self.desviacion, num_escenarios=-1)
        
        with self.assertRaises(ValueError):
            simular_tasas_inflacion(base_tasa=self.base_tasa, desviacion=self.desviacion, num_escenarios=0)
        
        with self.assertRaises(ValueError):
            simular_tasas_inflacion(base_tasa=self.base_tasa, desviacion=self.desviacion, num_escenarios=1000.5)
        
        with self.assertRaises(ValueError):
            simular_tasas_inflacion(base_tasa=self.base_tasa, desviacion=self.desviacion, num_escenarios="1000")

    def test_simular_flujos_bono_invalid_flujos(self):
        """
        Verifica que se levante una excepción si los flujos no son una lista.
        """
        with self.assertRaises(ValueError):
            simular_flujos_bono(flujos_originales=(100, 100, 1100), tasas_simuladas=self.tasas_simuladas, plazos=self.plazos)

    def test_simular_flujos_bono_flujos_vacio(self):
        """
        Verifica que se levante una excepción si la lista de flujos está vacía.
        """
        with self.assertRaises(ValueError):
            simular_flujos_bono(flujos_originales=[], tasas_simuladas=self.tasas_simuladas, plazos=self.plazos)

    def test_simular_flujos_bono_invalid_tasas_simuladas(self):
        """
        Verifica que se levante una excepción si las tasas simuladas no son un array 1D de NumPy.
        """
        with self.assertRaises(ValueError):
            simular_flujos_bono(flujos_originales=self.flujos, tasas_simuladas=[0.04, 0.05, 0.06], plazos=self.plazos)

    def test_simular_flujos_bono_tasas_simuladas_vacias(self):
        """
        Verifica que se levante una excepción si el array de tasas simuladas está vacío.
        """
        with self.assertRaises(ValueError):
            simular_flujos_bono(flujos_originales=self.flujos, tasas_simuladas=np.array([]), plazos=self.plazos)

    def test_simular_flujos_bono_invalid_plazos(self):
        """
        Verifica que se levante una excepción si los plazos no son una lista.
        """
        with self.assertRaises(ValueError):
            simular_flujos_bono(flujos_originales=self.flujos, tasas_simuladas=self.tasas_simuladas, plazos=(1, 2, 3))

    def test_simular_flujos_bono_plazos_vacio(self):
        """
        Verifica que se levante una excepción si la lista de plazos está vacía.
        """
        with self.assertRaises(ValueError):
            simular_flujos_bono(flujos_originales=self.flujos, tasas_simuladas=self.tasas_simuladas, plazos=[])

    def test_simular_flujos_bono_flujos_plazos_longitud_diferente(self):
        """
        Verifica que se levante una excepción si las listas de flujos y plazos no tienen la misma longitud.
        """
        with self.assertRaises(ValueError):
            simular_flujos_bono(flujos_originales=self.flujos, tasas_simuladas=self.tasas_simuladas, plazos=[1, 2])

if __name__ == '__main__':
    unittest.main()