from setuptools import setup, find_packages

setup(
    name="HW_MHS_pr0k4zn1k_tex_generator",  # Название вашего пакета на PyPI
    version="0.1.0",  # Версия
    description="Homework. A Python library for generating LaTeX tables and images",
    author="Edgar Oganisian",
    author_email="edgar21082000@yandex.ru",
    packages=find_packages(),
    install_requires=[],  # Зависимости
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",  # Минимальная версия Python
)
