# Bond Library

## Descripción
`pybono` es una biblioteca de Python diseñada para realizar cálculos y análisis relacionados con bonos financieros. Es ideal para analistas financieros, estudiantes de finanzas y desarrolladores interesados en ingeniería financiera. La biblioteca ofrece una amplia gama de herramientas para evaluar y gestionar portafolios de bonos, desde la valoración básica hasta análisis avanzados de riesgo y simulación de escenarios de tasas de interés.

## Instalación
Para instalar la biblioteca `pybono`, puedes utilizar `pip`:

pip install pybono=1.1.8

## Características Principales
## Valoración de Bonos
Calcula el precio de bonos, incluyendo bonos con cupones y bonos cero cupón. Esto permite determinar el valor actual de un bono basándose en sus flujos de caja y la tasa de descuento.

## Sensibilidad de Bonos
Calcula la duración de Macaulay, una medida de la sensibilidad del precio del bono a los cambios en las tasas de interés. También se pueden calcular otras medidas de sensibilidad como la convexidad.

## Cálculo de Tasa de Rendimiento al Vencimiento (YTM)
Determina la tasa de rendimiento anual esperada de un bono si se mantiene hasta la maduración. Esto es crucial para evaluar la rentabilidad de un bono.

## Generación de Flujos de Caja
Genera los flujos de caja de un bono, incluyendo pagos periódicos de cupones y el valor nominal al vencimiento. Esto ayuda a comprender los pagos futuros que recibirá el inversionista.

## Análisis de Portafolio de Bonos
Combina múltiples bonos para calcular el valor total del portafolio y su duración ponderada. Esto es útil para gestionar portafolios de bonos y equilibrar el riesgo.

## Análisis de Curva de Rendimiento
Evalúa la curva de rendimiento de bonos con diferentes maduridades, calculando sus YTMs y graficándolos. Esto permite analizar cómo cambian los rendimientos a medida que aumenta la maduración del bono.

## Medición de Riesgo
Calcula medidas de riesgo como la duración y la convexidad, que proporcionan información sobre la sensibilidad del bono a los cambios en las tasas de interés. Estas métricas son esenciales para evaluar el riesgo asociado con la inversión en bonos.

## Simulación de Escenarios de Tasas de Interés
Simula diferentes escenarios de tasas de interés y evalúa su impacto en los flujos de caja y los valores de los bonos. Esto ayuda a prever cómo podrían afectar los cambios en las tasas de interés a la inversión en bonos.

## Visualización
Genera visualizaciones para entender mejor los flujos de caja, las tasas de interés simuladas y otros análisis. Las visualizaciones incluyen gráficos de barras y histogramas que facilitan la interpretación de los resultados.

## Dependencias
La biblioteca pybono depende de las siguientes librerías:

numpy (versión >= 1.21.0)
pandas (versión >= 2.2.2)
matplotlib (versión >= 3.5.0)

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

## Contacto
Autor: Luis Humberto Calderon Baldeón <p>
Email: luis.calderon.b@uni.pe