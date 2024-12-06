# -*- coding: utf-8 -*-
"""
Simulación de rebalanceo.
Esta función ajusta un portafolio de bonos para alcanzar un objetivo de duración bajo ciertas restricciones y calcula los costos de transacción.
"""

def simular_rebalanceo(portafolio, objetivo_duracion, escenario_tasas, costos_transaccion=0.005):
    """
    Simula el rebalanceo de un portafolio de bonos para cumplir con un objetivo de duración.

    Args:
        portafolio (list): Lista de bonos, donde cada bono es un diccionario con claves:
            - "nombre": (str) Nombre del bono.
            - "precio": (float) Precio actual del bono.
            - "rendimiento": (float) Rendimiento esperado del bono.
            - "duracion": (float) Duración actual del bono.
        objetivo_duracion (float): Duración objetivo del portafolio.
        escenario_tasas (list): Lista de tasas de interés simuladas.
        costos_transaccion (float): Porcentaje de costos de transacción (por defecto: 0.5%).
        
    Returns:
        dict: Diccionario con claves:
            - "nuevo_portafolio": Lista de bonos ajustados.
            - "duracion_final": Duración del portafolio después del rebalanceo.
            - "costos_totales": Costos totales de transacción.
    """
    if not isinstance(portafolio, list) or not portafolio:
        raise ValueError("El portafolio debe ser una lista no vacía.")
    if not isinstance(objetivo_duracion, (int, float)):
        raise ValueError("El objetivo de duración debe ser un número.")
    if not isinstance(escenario_tasas, list) or not escenario_tasas:
        raise ValueError("El escenario de tasas debe ser una lista no vacía.")
    if not isinstance(costos_transaccion, (int, float)) or costos_transaccion < 0:
        raise ValueError("Los costos de transacción deben ser un número no negativo.")
    
    for bono in portafolio:
        if not isinstance(bono, dict):
            raise ValueError("Cada bono en el portafolio debe ser un diccionario.")
        required_keys = ["nombre", "precio", "rendimiento", "duracion"]
        for key in required_keys:
            if key not in bono:
                raise KeyError(f"Cada bono debe contener la clave '{key}'.")
        if not isinstance(bono["precio"], (int, float)) or bono["precio"] <= 0:
            raise ValueError("El precio del bono debe ser un número positivo.")
        if not isinstance(bono["rendimiento"], (int, float)):
            raise ValueError("El rendimiento del bono debe ser un número.")
        if not isinstance(bono["duracion"], (int, float)) or bono["duracion"] <= 0:
            raise ValueError("La duración del bono debe ser un número positivo.")
    
    # Calcular duración del portafolio actual
    total_valor_portafolio = sum(b["precio"] for b in portafolio)
    duracion_actual = sum(b["duracion"] * b["precio"] for b in portafolio) / total_valor_portafolio

    # Determinar si es necesario rebalancear
    if abs(duracion_actual - objetivo_duracion) < 0.01:  # Ya está cerca del objetivo
        return {
            "nuevo_portafolio": portafolio,
            "duracion_final": duracion_actual,
            "costos_totales": 0
        }

    # Rebalanceo: ajustar pesos del portafolio
    nuevo_portafolio = []
    costos_totales = 0

    for bono in portafolio:
        # Ajustar peso del bono para cumplir con la duración objetivo
        nuevo_peso = objetivo_duracion / bono["duracion"]
        nuevo_valor = nuevo_peso * total_valor_portafolio
        costo_transaccion = abs(nuevo_valor - bono["precio"]) * costos_transaccion

        nuevo_portafolio.append({
            "nombre": bono["nombre"],
            "precio": nuevo_valor,
            "rendimiento": bono["rendimiento"],
            "duracion": bono["duracion"]
        })
        costos_totales += costo_transaccion

    # Calcular la nueva duración del portafolio
    duracion_final = sum(b["duracion"] * b["precio"] for b in nuevo_portafolio) / total_valor_portafolio

    return {
        "nuevo_portafolio": nuevo_portafolio,
        "duracion_final": duracion_final,
        "costos_totales": costos_totales
    }