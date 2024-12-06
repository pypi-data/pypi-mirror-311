# -*- coding: utf-8 -*-
"""
Cálculo de Duración y Convexidad
"""

def calcular_duracion(flujos, tasa, plazos):
    """
    Calcula la duración de un bono.
    
    Args:
        flujos (list): Lista de flujos de efectivo.
        tasa (float): Tasa de descuento.
        plazos (list): Plazos en años para cada flujo.

    Returns:
        float: Duración del bono.
    """
    if not isinstance(flujos, list) or not flujos:
        raise ValueError("Los flujos deben ser una lista no vacía.")
    
    if not isinstance(tasa, (int, float)):
        raise ValueError("La tasa de descuento debe ser un número.")
    
    if not isinstance(plazos, list) or not plazos:
        raise ValueError("Los plazos deben ser una lista no vacía.")
    
    if len(flujos) != len(plazos):
        raise ValueError("Las listas de flujos y plazos deben tener la misma longitud.")
    
    valor_presente = sum(f / (1 + tasa)**t for f, t in zip(flujos, plazos))
    if valor_presente == 0:
        raise ValueError("El valor presente de los flujos es cero, lo que hace que la duración no esté definida.")
    
    duracion = sum((t * f) / (1 + tasa)**t for f, t in zip(flujos, plazos)) / valor_presente
    return duracion

def calcular_convexidad(flujos, tasa, plazos):
    """
    Calcula la convexidad de un bono.
    
    Args:
        flujos (list): Lista de flujos de efectivo.
        tasa (float): Tasa de descuento.
        plazos (list): Plazos en años para cada flujo.

    Returns:
        float: Convexidad del bono.
    """
    if not isinstance(flujos, list) or not flujos:
        raise ValueError("Los flujos deben ser una lista no vacía.")
    
    if not isinstance(tasa, (int, float)):
        raise ValueError("La tasa de descuento debe ser un número.")
    
    if not isinstance(plazos, list) or not plazos:
        raise ValueError("Los plazos deben ser una lista no vacía.")
    
    if len(flujos) != len(plazos):
        raise ValueError("Las listas de flujos y plazos deben tener la misma longitud.")
    
    valor_presente = sum(f / (1 + tasa)**t for f, t in zip(flujos, plazos))
    if valor_presente == 0:
        raise ValueError("El valor presente de los flujos es cero, lo que hace que la convexidad no esté definida.")
    
    convexidad = sum((t * (t + 1) * f) / (1 + tasa)**(t + 2) for f, t in zip(flujos, plazos)) / valor_presente
    return convexidad