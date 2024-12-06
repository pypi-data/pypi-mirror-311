from setuptools import setup, find_packages

setup(
    name="DWLFY",  # Nome do pacote no PyPI
    version="1.0.1", #Versão do pacote.
    description="The dwlfy library is a powerful and user-friendly tool designed to download videos from YouTube with options for video quality and format, along with an integrated MP3 conversion feature. This library is ideal for users who want flexibility in downloading, organizing, and converting YouTube content for offline use.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JkaiPrime/dwlfy",  # Link do repositório GitHub
    author="Lucas Guimaraes Moreira",
    author_email="lucasgmoreira002@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "yt-dlp",
        "ffmpeg"
    ],
)
