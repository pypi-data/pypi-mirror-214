from setuptools import setup, find_packages


with open("README.md", encoding="UTF-8") as file:
    readme = file.read()

with open("requirements.txt", "r", encoding="utf-8") as file:
    requirements = [line.strip() for line in file]

setup(
    name="lmt-cli",
    version="0.0.0",
    packages=find_packages(),
    install_requires=requirements,
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Sébastien De Revière",
)
