# -*- coding: utf-8 -*-
"""
Cálculo de la duración de Macaulay
"""

def duracion_macaulay(valor_nominal, tasa_cupon, tasa_descuento, periodos, frecuencia=1):
    """
    Calcula la duración de Macaulay de un bono.

    Args:
        valor_nominal (float): Valor nominal del bono.
        tasa_cupon (float): Tasa de cupón anual (en porcentaje).
        tasa_descuento (float): Tasa de descuento anual (en porcentaje).
        periodos (int): Número total de años hasta el vencimiento.
        frecuencia (int): Frecuencia de pago de cupones (1 = anual, 2 = semestral, etc.).

    Returns:
        float: Duración de Macaulay del bono.
    """
    if not isinstance(valor_nominal, (int, float)):
        raise ValueError("El valor nominal debe ser un número.")
    if not isinstance(tasa_cupon, (int, float)):
        raise ValueError("La tasa de cupón debe ser un número.")
    if not isinstance(tasa_descuento, (int, float)):
        raise ValueError("La tasa de descuento debe ser un número.")
    if not isinstance(periodos, int) or periodos <= 0:
        raise ValueError("El número de periodos debe ser un entero positivo.")
    if not isinstance(frecuencia, int) or frecuencia <= 0:
        raise ValueError("La frecuencia debe ser un entero positivo.")

    tasa_cupon /= 100
    tasa_descuento /= 100
    flujo_cupon = valor_nominal * tasa_cupon / frecuencia
    periodos_totales = periodos * frecuencia
    tasa_periodo = tasa_descuento / frecuencia

    # Calcular los flujos de efectivo descontados y sus pesos temporales
    flujos_descuentados = [
        (t, flujo_cupon / (1 + tasa_periodo) ** t) for t in range(1, periodos_totales + 1)
    ]
    flujos_descuentados.append((periodos_totales, valor_nominal / (1 + tasa_periodo) ** periodos_totales))

    # Numerador: Suma de tiempos ponderados por los flujos descontados
    numerador = sum(t * flujo for t, flujo in flujos_descuentados)

    # Denominador: Suma total de los flujos descontados
    denominador = sum(flujo for _, flujo in flujos_descuentados)

    if denominador == 0:
        raise ValueError("El valor presente de los flujos es cero, lo que hace que la duración no esté definida.")

    # Calcular la duración de Macaulay
    duracion = numerador / denominador

    return duracion