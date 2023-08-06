from setuptools import setup, find_packages

setup(
    name="BoKhalifaPackage",
    version="0.2",
    packages=find_packages(),
    author="Mshaeri Alkhalifa",
    author_email="mashari.khalifa@hotmail.com",
    description="A simple calculator package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="http://github.com/masharisk/BoKhalifaPackage",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
    ],
)