from setuptools import find_packages, setup
setup(
    name='consolegame',
    packages=find_packages(),
    version='0.0.4',
    description='A simple module to create a python console game',
    author='drooler',
    license='MIT',
    requires=["os", "sys", "time"]
)