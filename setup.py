from distutils.core import setup

setup(
    name="pymple",
    version="1.0",
    author="Andy Stanberry",
    author_email="andystanberry@gmail.com",
    url="https://github.com/cranberyxl/pymple",
    packages=["pymple"],
    license="Copyright 2013, Andy Stanberry under MIT License",
    description="Simple dependency injection container based on Pimple",
    long_description=open("README.md").read(),
)