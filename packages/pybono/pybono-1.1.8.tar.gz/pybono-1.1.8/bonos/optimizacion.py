# -*- coding: utf-8 -*-
"""
Comparación y Selección de Bonos
Analiza y elige el mejor bono según ciertos criterios.
"""

def comparar_bonos(bonos, tasa_descuento):
    """
    Compara múltiples bonos y selecciona el mejor basado en el Valor Presente Neto (VPN).
    
    Args:
        bonos (list): Lista de bonos, donde cada bono es un diccionario {'flujos': [...], 'plazos': [...]}
        tasa_descuento (float): Tasa de descuento aplicada a todos los bonos.
    
    Returns:
        dict: Bono con el mayor VPN.
    """
    if not isinstance(bonos, list) or not bonos:
        raise ValueError("La lista de bonos debe ser una lista no vacía.")
    
    if not isinstance(tasa_descuento, (int, float)):
        raise ValueError("La tasa de descuento debe ser un número.")
    
    resultados = []
    for bono in bonos:
        if not isinstance(bono, dict):
            raise ValueError("Cada bono debe ser un diccionario.")
        
        if 'flujos' not in bono or 'plazos' not in bono:
            raise KeyError("Cada bono debe contener las claves 'flujos' y 'plazos'.")
        
        flujos = bono['flujos']
        plazos = bono['plazos']
        
        if not isinstance(flujos, list) or not isinstance(plazos, list):
            raise ValueError("Los flujos y plazos deben ser listas.")
        
        if len(flujos) != len(plazos):
            raise ValueError("Las listas de flujos y plazos deben tener la misma longitud.")
        
        vpn = sum(f / (1 + tasa_descuento)**t for f, t in zip(flujos, plazos))
        resultados.append({'bono': bono, 'vpn': vpn})
    
    # Seleccionar el bono con el mayor VPN
    mejor_bono = max(resultados, key=lambda x: x['vpn'])
    return mejor_bono