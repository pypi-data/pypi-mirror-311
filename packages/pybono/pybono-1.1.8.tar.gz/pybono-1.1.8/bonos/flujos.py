# -*- coding: utf-8 -*-
"""
Generación de Flujos de Caja
Los flujos de caja de un bono consisten en:

Pagos periódicos de cupones, que se calculan como la tasa de cupón multiplicada por el valor nominal.
El valor nominal del bono, que se paga al vencimiento.
El flujo de caja tiene en cuenta:

Frecuencia: Si el bono paga cupones anualmente, semestralmente, trimestralmente, etc.
Duración: Número de años hasta el vencimiento.
Tasa de cupón: La tasa anual expresada como porcentaje del valor nominal.
Valor nominal: El monto principal que se paga al vencimiento.
"""

def generar_flujos(valor_nominal, tasa_cupon, periodos, frecuencia=1):
    """
    Genera los flujos de caja de un bono.

    Args:
        valor_nominal (float): Valor nominal del bono.
        tasa_cupon (float): Tasa de cupón anual (en porcentaje).
        periodos (int): Número total de años hasta el vencimiento.
        frecuencia (int): Frecuencia de pago de cupones (1 = anual, 2 = semestral, etc.).

    Returns:
        list: Lista de flujos de caja, donde cada elemento representa un pago en un periodo.
    """
    if not isinstance(valor_nominal, (int, float)):
        raise ValueError("El valor nominal debe ser un número.")
    if not isinstance(tasa_cupon, (int, float)):
        raise ValueError("La tasa de cupón debe ser un número.")
    if not isinstance(periodos, int) or periodos <= 0:
        raise ValueError("El número de periodos debe ser un entero positivo.")
    if not isinstance(frecuencia, int) or frecuencia <= 0:
        raise ValueError("La frecuencia debe ser un entero positivo.")

    tasa_cupon /= 100  # Convertir la tasa de cupón a decimal
    flujo_cupon = valor_nominal * tasa_cupon / frecuencia
    flujos = [flujo_cupon] * (periodos * frecuencia)  # Cupones periódicos
    flujos[-1] += valor_nominal  # Agregar el valor nominal al último flujo
    return flujos