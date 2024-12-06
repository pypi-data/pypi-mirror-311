# -*- coding: utf-8 -*-
"""
Gráficos y Visualización
"""

import matplotlib.pyplot as plt

def graficar_flujos(flujos, plazos):
    """
    Genera un gráfico de barras para visualizar los flujos de efectivo del bono.
    
    Args:
        flujos (list): Lista de flujos de efectivo.
        plazos (list): Lista de plazos correspondientes.
    """
    if not isinstance(flujos, list) or not flujos:
        raise ValueError("Los flujos deben ser una lista no vacía.")
    if not isinstance(plazos, list) or not plazos:
        raise ValueError("Los plazos deben ser una lista no vacía.")
    if len(flujos) != len(plazos):
        raise ValueError("Las listas de flujos y plazos deben tener la misma longitud.")
    
    plt.figure(figsize=(10, 6))
    plt.bar(plazos, flujos, color='skyblue', edgecolor='black')
    plt.xlabel('Plazos (años)')
    plt.ylabel('Flujos de Efectivo')
    plt.title('Flujos de Efectivo del Bono')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(plazos)  # Asegura que los plazos se muestren en el eje x
    plt.tight_layout()  # Ajusta el diseño para evitar recortes
    plt.show()

def graficar_tasas_simuladas(tasas_simuladas):
    """
    Genera un histograma de las tasas simuladas.
    
    Args:
        tasas_simuladas (list): Lista de tasas simuladas.
    """
    if not isinstance(tasas_simuladas, list) or not tasas_simuladas:
        raise ValueError("Las tasas simuladas deben ser una lista no vacía.")
    
    plt.figure(figsize=(10, 6))
    plt.hist(tasas_simuladas, bins=20, color='lightgreen', edgecolor='black')
    plt.xlabel('Tasas de Interés')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de Tasas Simuladas')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()  # Ajusta el diseño para evitar recortes
    plt.show()