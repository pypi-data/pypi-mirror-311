from setuptools import setup, find_packages

setup(
    name="data_search_engine",  # Nazwa pakietu
    version="1.0.2",  # Wersja
    description="A Python-based data search and visualization engine.",  # Opis
    long_description=open("README.md", "r", encoding="utf-8").read(),  # Szczegóły z README
    long_description_content_type="text/markdown",  # Format opisu
    author="Siatek98",  # Twoje imię/nazwa
    url="https://github.com/Siatek98/data_search_engine",  # Link do repozytorium
    packages=find_packages(),  # Automatyczne znajdowanie modułów
    include_package_data=True,  # Dołączenie dodatkowych plików (np. README.md)
    install_requires=open("requirements.txt", "r", encoding="utf-8").read().splitlines(),  # Zależności
    python_requires=">=3.6",  # Minimalna wersja Pythona
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
