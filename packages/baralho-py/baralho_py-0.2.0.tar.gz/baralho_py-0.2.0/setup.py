from setuptools import setup, find_packages

setup(
    name="baralho-py",  # Nome do pacote
    version="0.2.0",  # Versão inicial
    author="Arthur Felipe",
    author_email="arthurfelipe5567@gmail.com",
    description="Jogo simples de batalha.",
    long_description="Jogo simples de batalha.",
    long_description_content_type="text/markdown",
    url="https://github.com/arthurfaraujo/ed",  # URL do repositório (opcional)
    packages=find_packages(),  # Encontra automaticamente subpacotes
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Dependências do pacote (ex: 'requests', 'numpy')
    ],
    entry_points={
      "console_scripts": ["baralho-py=baralho_py.main:main"]
    }
)
