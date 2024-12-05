from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
    name="Haack4uu",
    version="3.1.8",
    packages=find_packages(),
    install_requires=[],
    author="CP",
    description="Biblioteca para practicar.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io"
)
