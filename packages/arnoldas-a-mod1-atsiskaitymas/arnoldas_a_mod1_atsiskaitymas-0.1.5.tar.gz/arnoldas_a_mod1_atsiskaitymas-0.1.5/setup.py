from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="arnoldas_a_mod1_atsiskaitymas",
    version="0.1.5",
    description="A Python project for scraping book info and football results",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Arnoldas A.",
    author_email="ambrasas.arnoldas@gmail.com",
    url="https://github.com/Asasai001/arnoldas-a-mod1-atsiskaitymas",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "pandas",
    ],
    python_requires=">=3.10"
)