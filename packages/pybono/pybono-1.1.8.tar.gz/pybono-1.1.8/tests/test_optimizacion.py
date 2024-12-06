# -*- coding: utf-8 -*-
"""
Pruebas para las funciones de comparación de bonos y selección del mejor bono.
"""

import unittest
from bonos.optimizacion import comparar_bonos

class TestOptimizacion(unittest.TestCase):
    def setUp(self):
        # Configuramos algunos bonos ficticios para la prueba
        self.bonos = [
            {'flujos': [100, 100, 1100], 'plazos': [1, 2, 3]},  # Bono 1
            {'flujos': [50, 50, 1050], 'plazos': [1, 2, 3]},   # Bono 2
            {'flujos': [200, 200, 1200], 'plazos': [1, 2, 3]}  # Bono 3
        ]
        self.tasa_descuento = 0.05  # 5%

    def test_comparar_bonos(self):
        # Llamamos a la función para comparar los bonos
        mejor_bono = comparar_bonos(self.bonos, self.tasa_descuento)
        
        # Verificamos que el bono con el mayor Valor Presente Neto es el Bono 3
        self.assertEqual(mejor_bono['bono'], self.bonos[2])  # Verificar que seleccionó el bono correcto
        self.assertAlmostEqual(mejor_bono['vpn'], 1464.11, places=2)  # Verificar el VPN del mejor bono

    def test_bono_con_menos_flujos(self):
        """
        Verifica que se levante una excepción si los flujos y plazos no tienen la misma longitud.
        """
        bonos_invalidos = [
            {'flujos': [100, 100], 'plazos': [1, 2, 3]},  # Bono con menos flujos
            {'flujos': [50, 50, 1050], 'plazos': [1, 2, 3]},   # Bono válido
            {'flujos': [200, 200, 1200], 'plazos': [1, 2, 3]}  # Bono válido
        ]
        with self.assertRaises(ValueError):
            comparar_bonos(bonos_invalidos, self.tasa_descuento)

    def test_bono_con_tipo_incorrecto(self):
        """
        Verifica que se levante una excepción si los bonos no son diccionarios.
        """
        bonos_invalidos = [
            [100, 100, 1100],  # Bono inválido
            {'flujos': [50, 50, 1050], 'plazos': [1, 2, 3]},   # Bono válido
            {'flujos': [200, 200, 1200], 'plazos': [1, 2, 3]}  # Bono válido
        ]
        with self.assertRaises(ValueError):
            comparar_bonos(bonos_invalidos, self.tasa_descuento)

    def test_flujos_no_lista(self):
        """
        Verifica que se levante una excepción si los flujos no son una lista.
        """
        bonos_invalidos = [
            {'flujos': (100, 100, 1100), 'plazos': [1, 2, 3]},  # Bono inválido
            {'flujos': [50, 50, 1050], 'plazos': [1, 2, 3]},   # Bono válido
            {'flujos': [200, 200, 1200], 'plazos': [1, 2, 3]}  # Bono válido
        ]
        with self.assertRaises(ValueError):
            comparar_bonos(bonos_invalidos, self.tasa_descuento)

    def test_plazos_no_lista(self):
        """
        Verifica que se levante una excepción si los plazos no son una lista.
        """
        bonos_invalidos = [
            {'flujos': [100, 100, 1100], 'plazos': (1, 2, 3)},  # Bono inválido
            {'flujos': [50, 50, 1050], 'plazos': [1, 2, 3]},   # Bono válido
            {'flujos': [200, 200, 1200], 'plazos': [1, 2, 3]}  # Bono válido
        ]
        with self.assertRaises(ValueError):
            comparar_bonos(bonos_invalidos, self.tasa_descuento)

    def test_sin_clave_flujos(self):
        """
        Verifica que se levante una excepción si falta la clave 'flujos'.
        """
        bonos_invalidos = [
            {'plazos': [1, 2, 3]},  # Bono inválido
            {'flujos': [50, 50, 1050], 'plazos': [1, 2, 3]},   # Bono válido
            {'flujos': [200, 200, 1200], 'plazos': [1, 2, 3]}  # Bono válido
        ]
        with self.assertRaises(KeyError):
            comparar_bonos(bonos_invalidos, self.tasa_descuento)

    def test_sin_clave_plazos(self):
        """
        Verifica que se levante una excepción si falta la clave 'plazos'.
        """
        bonos_invalidos = [
            {'flujos': [100, 100, 1100]},  # Bono inválido
            {'flujos': [50, 50, 1050], 'plazos': [1, 2, 3]},   # Bono válido
            {'flujos': [200, 200, 1200], 'plazos': [1, 2, 3]}  # Bono válido
        ]
        with self.assertRaises(KeyError):
            comparar_bonos(bonos_invalidos, self.tasa_descuento)

    def test_tasa_descuento_invalida(self):
        """
        Verifica que se levante una excepción si la tasa de descuento no es un número.
        """
        with self.assertRaises(ValueError):
            comparar_bonos(self.bonos, "0.05")

    def test_bonos_vacia(self):
        """
        Verifica que se levante una excepción si la lista de bonos está vacía.
        """
        bonos_vacia = []
        with self.assertRaises(ValueError):
            comparar_bonos(bonos_vacia, self.tasa_descuento)

if __name__ == '__main__':
    unittest.main()