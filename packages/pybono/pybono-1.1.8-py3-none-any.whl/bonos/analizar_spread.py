# -*- coding: utf-8 -*-
"""
Análisis de Spread de Bonos Corporativos vs. Gubernamentales
Esta función calcula el spread de rendimiento entre un bono corporativo y uno gubernamental
con características similares. También analiza cómo varía el spread bajo diferentes tasas de descuento.
"""
#%%
def calcular_rendimiento(precio, valor_nominal, tasa_cupon, periodos, tasa_descuento):
    """
    Calcula el rendimiento de un bono dado su precio, valor nominal, tasa de cupón,
    número de periodos y tasa de descuento.

    Args:
        precio (float): Precio actual del bono.
        valor_nominal (float): Valor nominal del bono.
        tasa_cupon (float): Tasa de cupón del bono.
        periodos (int): Número de periodos hasta el vencimiento.
        tasa_descuento (float): Tasa de descuento.

    Returns:
        float: Rendimiento del bono.
    """
    flujo_cupon = tasa_cupon * valor_nominal
    rendimiento = sum(flujo_cupon / (1 + tasa_descuento)**t for t in range(1, periodos + 1)) + \
                  valor_nominal / (1 + tasa_descuento)**periodos
    return rendimiento

def analizar_spread(bono_corporativo, bono_gubernamental, tasas_descuento):
    """
    Analiza el spread entre el rendimiento de un bono corporativo y uno gubernamental.

    Args:
        bono_corporativo (dict): Diccionario con los detalles del bono corporativo:
            - "precio": (float) Precio actual del bono.
            - "valor_nominal": (float) Valor nominal del bono.
            - "tasa_cupon": (float) Tasa de cupón del bono.
            - "periodos": (int) Número de periodos hasta el vencimiento.
        bono_gubernamental (dict): Diccionario con los mismos detalles que el bono corporativo.
        tasas_descuento (list): Lista de tasas de descuento para evaluar el spread.

    Returns:
        dict: Diccionario con:
            - "spreads": Lista de spreads calculados.
            - "promedio": Spread promedio.
            - "minimo": Spread mínimo.
            - "maximo": Spread máximo.
    """
    if not isinstance(bono_corporativo, dict) or not isinstance(bono_gubernamental, dict):
        raise ValueError("Los bonos deben ser diccionarios.")
    
    required_keys = ["precio", "valor_nominal", "tasa_cupon", "periodos"]
    for key in required_keys:
        if key not in bono_corporativo or key not in bono_gubernamental:
            raise KeyError(f"Falta la clave '{key}' en uno de los bonos.")
    
    if not isinstance(tasas_descuento, list) or not all(isinstance(t, (int, float)) for t in tasas_descuento):
        raise ValueError("Las tasas de descuento deben ser una lista de números.")
    
    spreads = []
    for tasa in tasas_descuento:
        rendimiento_corporativo = calcular_rendimiento(
            bono_corporativo["precio"], 
            bono_corporativo["valor_nominal"], 
            bono_corporativo["tasa_cupon"], 
            bono_corporativo["periodos"], 
            tasa
        )
        rendimiento_gubernamental = calcular_rendimiento(
            bono_gubernamental["precio"], 
            bono_gubernamental["valor_nominal"], 
            bono_gubernamental["tasa_cupon"], 
            bono_gubernamental["periodos"], 
            tasa
        )
        spreads.append(rendimiento_corporativo - rendimiento_gubernamental)
    
    return {
        "spreads": spreads,
        "promedio": sum(spreads) / len(spreads),
        "minimo": min(spreads),
        "maximo": max(spreads)
    }
#%%