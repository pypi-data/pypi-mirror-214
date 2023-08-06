from setuptools import find_packages, setup
setup(
    name='consolegame',
    packages=find_packages("./src"),
    version='0.0.3',
    description='A simple module to create a python console game',
    author='drooler',
    license='MIT',
    requires=["os", "sys", "time"]
)