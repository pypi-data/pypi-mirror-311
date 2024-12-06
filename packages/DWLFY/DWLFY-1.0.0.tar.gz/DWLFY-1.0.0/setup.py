from setuptools import setup, find_packages

setup(
    name="DWLFY",  # Nome do pacote no PyPI
    version="1.0.0", #Versão do pacote.
    description="The dwlfy library is a powerful and user-friendly tool designed to download videos from YouTube with options for video quality and format, along with an integrated MP3 conversion feature. This library is ideal for users who want flexibility in downloading, organizing, and converting YouTube content for offline use.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seu_usuario/my_library",  # Link do repositório GitHub
    author="Seu Nome",
    author_email="seu_email@example.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),  # Descobre e inclui todos os pacotes no diretório
    python_requires=">=3.6",  # Versão mínima do Python suportada
    install_requires=[
        # Dependências necessárias para sua biblioteca
        "requests",
        "numpy"
    ],
)
