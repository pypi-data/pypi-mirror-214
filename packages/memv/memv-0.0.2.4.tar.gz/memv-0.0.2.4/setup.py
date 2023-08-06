
from setuptools import setup, find_packages

setup(
    name='memv',
    version='0.0.2.4',
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