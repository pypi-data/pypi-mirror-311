from setuptools import setup, find_packages

setup(
    name="yahel",  # Nome único do package no PyPI
    version="0.1.0",  # Número da versão
    packages=find_packages(),  # Inclui todos os submódulos
    install_requires=["matplotlib", "numpy", "seaborn"],  # Dependências
    description="Pacote para visualização de dados com mapas de calor, gráficos de pizza e gráficos de área.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Luiz 441",
    author_email="osramosdejesus1990@gmail.com",
    url="https://github.com/luiz441/yahel",  # Repositório no GitHub (opcional)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Versões suportadas do Python
)