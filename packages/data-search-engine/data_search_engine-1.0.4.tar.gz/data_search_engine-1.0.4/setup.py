from setuptools import setup, find_packages

setup(
    name="data_search_engine",
    version="1.0.4",  # Nowa wersja
    description="A Python-based data search and visualization engine.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Siatek98",
    url="https://github.com/Siatek98/data_search_engine",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas",
        "matplotlib",
        "fredapi",
        "pyperclip",
        "yfinance",
        "requests",
        "reportlab",
        "openpyxl",
        "eurostat",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "gui": ["tk"],  # Użytkownicy mogą to dodać ręcznie, jeśli zajdzie potrzeba
    },
)
