import setuptools
from pathlib import Path


long_desc = Path("README.md").read_text()

setuptools.setup(
    # Nombre del paquete dentro de pipy
    name="holamundoplayer-fabeliz",
    version="0.0.1",
    # importar lo que esta en README aqui
    long_description=long_desc,
    packages=setuptools.find_packages(
        # Paquetes a ignorar
        exclude=["mocks", "tests"]
    )
)
