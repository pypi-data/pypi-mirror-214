
from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='CToolKit',
    version='1.13',
    description='CToolKit to manipulate CPipeLines and Repos',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Mateus Moutinho',
    author_email='mateusmoutinho01@gmail.com',
    url='https://oui.tec.br/',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)