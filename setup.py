from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Pombos_brabos",  # Nome do seu projeto
    version="0.1.0",
    author="Marcelo e Henrique",  # Nome do autor do projeto
    author_email="mclonso123@outlook.com",  # Email do autor
    description="Projeto de alglin",  # Descrição do projeto
    long_description=long_description,
    long_description_content_type="text/markdown",  # Tipo de conteúdo da descrição longa
    url="https://github.com/Marcelo-vta/Pombos_brabos",  # URL do repositório do projeto
    packages=find_packages(),  # Pacotes a serem incluídos na distribuição
    classifiers=[  # Classificadores para facilitar a busca do projeto
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    entry_points={
        'console_scripts': [
            'marcelo_pombos_brabos=Pombos_brabos.main:main',
        ],
    },

    install_requires=[  # Instala as dependências especificadas no requirements.txt
        line.strip() for line in open("requirements.txt").readlines()
    ],
)