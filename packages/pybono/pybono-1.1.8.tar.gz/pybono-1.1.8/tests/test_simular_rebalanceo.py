# -*- coding: utf-8 -*-
"""
Pruebas para las funciones de simulación de rebalanceo.
"""

import unittest
from bonos.portafolio import simular_rebalanceo

class TestSimularRebalanceo(unittest.TestCase):
    def setUp(self):
        # Configuramos un portafolio inicial para las pruebas
        self.portafolio = [
            {"nombre": "Bono 1", "precio": 900, "rendimiento": 0.04, "duracion": 3.5},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        self.objetivo_duracion = 4.0
        self.escenario_tasas = [0.03, 0.04, 0.05]
        self.costos_transaccion = 0.005

    def test_rebalanceo_correcto(self):
        """
        Verifica que la función ajuste correctamente el portafolio para alcanzar la duración objetivo.
        """
        resultados = simular_rebalanceo(
            portafolio=self.portafolio, 
            objetivo_duracion=self.objetivo_duracion, 
            escenario_tasas=self.escenario_tasas, 
            costos_transaccion=self.costos_transaccion
        )

        # La duración final debe estar cerca del objetivo
        self.assertAlmostEqual(resultados["duracion_final"], self.objetivo_duracion, places=1)
        
        # El nuevo portafolio debe tener un número igual de bonos
        self.assertEqual(len(resultados["nuevo_portafolio"]), len(self.portafolio))
        
        # Los costos de transacción deben ser mayores a 0
        self.assertGreater(resultados["costos_totales"], 0)

    def test_costos_transaccion(self):
        """
        Verifica que los costos de transacción sean calculados correctamente.
        """
        resultados = simular_rebalanceo(
            portafolio=self.portafolio, 
            objetivo_duracion=self.objetivo_duracion, 
            escenario_tasas=self.escenario_tasas, 
            costos_transaccion=self.costos_transaccion
        )

        # Verificar que los costos sean un número mayor a 0
        self.assertGreater(resultados["costos_totales"], 0)
        self.assertIsInstance(resultados["costos_totales"], float)

    def test_sin_rebalanceo_necesario(self):
        """
        Verifica que no se realice rebalanceo si el portafolio ya cumple con el objetivo de duración.
        """
        objetivo_duracion = 3.5  # Igual a la duración promedio actual
        resultados = simular_rebalanceo(
            portafolio=self.portafolio, 
            objetivo_duracion=objetivo_duracion, 
            escenario_tasas=self.escenario_tasas, 
            costos_transaccion=self.costos_transaccion
        )

        # No debe haber costos de transacción
        self.assertEqual(resultados["costos_totales"], 0)
        
        # La duración final debe ser igual al objetivo
        self.assertEqual(resultados["duracion_final"], objetivo_duracion)
        
        # El portafolio no debe cambiar
        self.assertEqual(resultados["nuevo_portafolio"], self.portafolio)

    def test_invalid_portafolio(self):
        """
        Verifica que se levante una excepción si el portafolio no es una lista.
        """
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio="no_es_una_lista", objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_portafolio_vacio(self):
        """
        Verifica que se levante una excepción si el portafolio está vacío.
        """
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=[], objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_invalid_objetivo_duracion(self):
        """
        Verifica que se levante una excepción si el objetivo de duración no es un número.
        """
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=self.portafolio, objetivo_duracion="no_es_un_numero", escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_invalid_escenario_tasas(self):
        """
        Verifica que se levante una excepción si el escenario de tasas no es una lista.
        """
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=self.portafolio, objetivo_duracion=self.objetivo_duracion, escenario_tasas="no_es_una_lista", costos_transaccion=self.costos_transaccion)

    def test_escenario_tasas_vacio(self):
        """
        Verifica que se levante una excepción si el escenario de tasas está vacío.
        """
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=self.portafolio, objetivo_duracion=self.objetivo_duracion, escenario_tasas=[], costos_transaccion=self.costos_transaccion)

    def test_invalid_costos_transaccion(self):
        """
        Verifica que se levante una excepción si los costos de transacción no son un número no negativo.
        """
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=self.portafolio, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion="no_es_un_numero")
        
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=self.portafolio, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=-0.01)

    def test_invalid_bono_formato(self):
        """
        Verifica que se levante una excepción si los bonos no son diccionarios.
        """
        portafolio_invalido = [
            ["Bono 1", 900, 0.04, 3.5],
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_bono_sin_clave(self):
        """
        Verifica que se levante una excepción si los bonos faltan alguna clave.
        """
        portafolio_invalido = [
            {"nombre": "Bono 1", "precio": 900, "rendimiento": 0.04},  # Falta "duracion"
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(KeyError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_bono_precio_invalido(self):
        """
        Verifica que se levante una excepción si el precio del bono no es un número positivo.
        """
        portafolio_invalido = [
            {"nombre": "Bono 1", "precio": -900, "rendimiento": 0.04, "duracion": 3.5},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_bono_rendimiento_invalido(self):
        """
        Verifica que se levante una excepción si el rendimiento del bono no es un número.
        """
        portafolio_invalido = [
            {"nombre": "Bono 1", "precio": 900, "rendimiento": "0.04", "duracion": 3.5},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_bono_duracion_invalida(self):
        """
        Verifica que se levante una excepción si la duración del bono no es un número positivo.
        """
        portafolio_invalido = [
            {"nombre": "Bono 1", "precio": 900, "rendimiento": 0.04, "duracion": -3.5},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_bono_duracion_cero(self):
        """
        Verifica que se levante una excepción si la duración del bono es cero.
        """
        portafolio_invalido = [
            {"nombre": "Bono 1", "precio": 900, "rendimiento": 0.04, "duracion": 0},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_bono_duracion_negativa(self):
        """
        Verifica que se levante una excepción si la duración del bono es negativa.
        """
        portafolio_invalido = [
            {"nombre": "Bono 1", "precio": 900, "rendimiento": 0.04, "duracion": -3.5},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_bono_precio_cero(self):
        """
        Verifica que se levante una excepción si el precio del bono es cero.
        """
        portafolio_invalido = [
            {"nombre": "Bono 1", "precio": 0, "rendimiento": 0.04, "duracion": 3.5},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_bono_precio_negativo(self):
        """
        Verifica que se levante una excepción si el precio del bono es negativo.
        """
        portafolio_invalido = [
            {"nombre": "Bono 1", "precio": -900, "rendimiento": 0.04, "duracion": 3.5},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_bono_rendimiento_negativo(self):
        """
        Verifica que se levante una excepción si el rendimiento del bono es negativo.
        """
        portafolio_invalido = [
            {"nombre": "Bono 1", "precio": 900, "rendimiento": -0.04, "duracion": 3.5},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_bono_rendimiento_no_numero(self):
        """
        Verifica que se levante una excepción si el rendimiento del bono no es un número.
        """
        portafolio_invalido = [
            {"nombre": "Bono 1", "precio": 900, "rendimiento": "0.04", "duracion": 3.5},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_bono_duracion_no_numero(self):
        """
        Verifica que se levante una excepción si la duración del bono no es un número.
        """
        portafolio_invalido = [
            {"nombre": "Bono 1", "precio": 900, "rendimiento": 0.04, "duracion": "3.5"},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_bono_nombre_invalido(self):
        """
        Verifica que se levante una excepción si el nombre del bono no es una cadena.
        """
        portafolio_invalido = [
            {"nombre": 123, "precio": 900, "rendimiento": 0.04, "duracion": 3.5},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_bono_nombre_vacio(self):
        """
        Verifica que se levante una excepción si el nombre del bono es una cadena vacía.
        """
        portafolio_invalido = [
            {"nombre": "", "precio": 900, "rendimiento": 0.04, "duracion": 3.5},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_bono_precio_no_numero(self):
        """
        Verifica que se levante una excepción si el precio del bono no es un número.
        """
        portafolio_invalido = [
            {"nombre": "Bono 1", "precio": "900", "rendimiento": 0.04, "duracion": 3.5},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_bono_precio_no_positivo(self):
        """
        Verifica que se levante una excepción si el precio del bono no es positivo.
        """
        portafolio_invalido = [
            {"nombre": "Bono 1", "precio": 0, "rendimiento": 0.04, "duracion": 3.5},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

        portafolio_invalido = [
            {"nombre": "Bono 1", "precio": -900, "rendimiento": 0.04, "duracion": 3.5},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_bono_duracion_no_positivo(self):
        """
        Verifica que se levante una excepción si la duración del bono no es positiva.
        """
        portafolio_invalido = [
            {"nombre": "Bono 1", "precio": 900, "rendimiento": 0.04, "duracion": 0},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

        portafolio_invalido = [
            {"nombre": "Bono 1", "precio": 900, "rendimiento": 0.04, "duracion": -3.5},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        with self.assertRaises(ValueError):
            simular_rebalanceo(portafolio=portafolio_invalido, objetivo_duracion=self.objetivo_duracion, escenario_tasas=self.escenario_tasas, costos_transaccion=self.costos_transaccion)

    def test_rebalanceo_con_escalado(self):
        """
        Verifica que el rebalanceo ajuste correctamente los pesos de los bonos para alcanzar la duración objetivo.
        """
        portafolio = [
            {"nombre": "Bono 1", "precio": 900, "rendimiento": 0.04, "duracion": 3.5},
            {"nombre": "Bono 2", "precio": 950, "rendimiento": 0.05, "duracion": 5.0},
            {"nombre": "Bono 3", "precio": 1000, "rendimiento": 0.03, "duracion": 2.0}
        ]
        objetivo_duracion = 4.0
        escenario_tasas = [0.03, 0.04, 0.05]
        resultados = simular_rebalanceo(
            portafolio=portafolio, 
            objetivo_duracion=objetivo_duracion, 
            escenario_tasas=escenario_tasas, 
            costos_transaccion=self.costos_transaccion
        )

        # La duración final debe estar cerca del objetivo
        self.assertAlmostEqual(resultados["duracion_final"], objetivo_duracion, places=1)
        
        # El nuevo portafolio debe tener un número igual de bonos
        self.assertEqual(len(resultados["nuevo_portafolio"]), len(portafolio))
        
        # Los costos de transacción deben ser mayores a 0
        self.assertGreater(resultados["costos_totales"], 0)

    def test_rebalanceo_sin_costos(self):
        """
        Verifica que no haya costos de transacción si el portafolio ya cumple con el objetivo de duración.
        """
        objetivo_duracion = 3.5  # Igual a la duración promedio actual
        resultados = simular_rebalanceo(
            portafolio=self.portafolio, 
            objetivo_duracion=objetivo_duracion, 
            escenario_tasas=self.escenario_tasas, 
            costos_transaccion=self.costos_transaccion
        )

        # No debe haber costos de transacción
        self.assertEqual(resultados["costos_totales"], 0)
        
        # La duración final debe ser igual al objetivo
        self.assertEqual(resultados["duracion_final"], objetivo_duracion)
        
        # El portafolio no debe cambiar
        self.assertEqual(resultados["nuevo_portafolio"], self.portafolio)

if __name__ == '__main__':
    unittest.main()