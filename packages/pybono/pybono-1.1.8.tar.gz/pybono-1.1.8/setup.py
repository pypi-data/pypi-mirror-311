"""
Setup script for pybono package
"""

from setuptools import setup, find_packages

# Lee el archivo README.md con la codificación correcta
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pybono",  # Nombre del paquete
    version="1.1.8",  # Versión inicial
    description="Librería para análisis y cálculos de bonos financieros",
    long_description=long_description,  # Utiliza el contenido leído de README.md
    long_description_content_type="text/markdown",  # Tipo de contenido de la descripción larga
    url="https://github.com/LuisHCalderon/pybono",  # URL de tu repositorio
    author="Luis Humberto Calderon Baldeón",
    author_email="luis.calderon.b@uni.pe",  
    license="MIT",  # Licencia
    packages=find_packages(),  # Encuentra automáticamente los paquetes
    install_requires=[
        'numpy>=1.21.0',          # Para cálculos matemáticos
        'pandas>=2.2.2',            # Manipulación y análisis de datos
        'matplotlib>=3.5.0',      # Para visualización de datos
    ],
    python_requires='>=3.7',  # Versión mínima de Python requerida
    keywords='bond financial analysis yield to maturity duration convexity',
)