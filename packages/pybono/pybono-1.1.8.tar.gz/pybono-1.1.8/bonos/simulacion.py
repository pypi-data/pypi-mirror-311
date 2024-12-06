# -*- coding: utf-8 -*-
"""
Simulación de Escenarios

Este módulo contiene funciones para simular diferentes escenarios de tasas de interés y calcular los valores presentes de los flujos de un bono bajo esos escenarios.
"""

import numpy as np

def simular_tasas_inflacion(base_tasa, desviacion, num_escenarios=100):
    """
    Simula diferentes escenarios para tasas de interés basadas en una distribución normal.
    
    Args:
        base_tasa (float): Tasa de interés base (promedio esperado).
        desviacion (float): Desviación estándar de las tasas simuladas.
        num_escenarios (int): Número de escenarios a simular.
    
    Returns:
        np.array: Array con las tasas simuladas.
    """
    if not isinstance(base_tasa, (int, float)):
        raise ValueError("La tasa base debe ser un número.")
    if not isinstance(desviacion, (int, float)):
        raise ValueError("La desviación estándar debe ser un número.")
    if not isinstance(num_escenarios, int) or num_escenarios <= 0:
        raise ValueError("El número de escenarios debe ser un entero positivo.")
    
    tasas_simuladas = np.random.normal(loc=base_tasa, scale=desviacion, size=num_escenarios)
    return tasas_simuladas

def simular_flujos_bono(flujos_originales, tasas_simuladas, plazos):
    """
    Calcula los valores presentes de los flujos de un bono bajo diferentes escenarios de tasas.
    
    Args:
        flujos_originales (list): Lista de flujos de efectivo originales del bono.
        tasas_simuladas (np.array): Array de tasas simuladas.
        plazos (list): Plazos en años correspondientes a cada flujo.
    
    Returns:
        list: Lista de valores presentes de los flujos bajo cada escenario.
    """
    if not isinstance(flujos_originales, list) or not flujos_originales:
        raise ValueError("Los flujos originales deben ser una lista no vacía.")
    if not isinstance(tasas_simuladas, np.ndarray) or tasas_simuladas.ndim != 1:
        raise ValueError("Las tasas simuladas deben ser un array 1D de NumPy.")
    if not isinstance(plazos, list) or not plazos:
        raise ValueError("Los plazos deben ser una lista no vacía.")
    if len(flujos_originales) != len(plazos):
        raise ValueError("Las listas de flujos y plazos deben tener la misma longitud.")
    
    escenarios_flujos = []
    for tasa in tasas_simuladas:
        flujos_descuento = [f / (1 + tasa)**t for f, t in zip(flujos_originales, plazos)]
        escenarios_flujos.append(flujos_descuento)
    return escenarios_flujos