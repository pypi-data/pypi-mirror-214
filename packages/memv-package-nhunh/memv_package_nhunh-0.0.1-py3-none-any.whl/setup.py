
from setuptools import setup, find_packages

setup(
    name='mem_visualize',
    version='0.0.1',
    description='Create graph to visualize memory usage',
    author='nhunh',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'memv=memv:main',
        ],
    },
)