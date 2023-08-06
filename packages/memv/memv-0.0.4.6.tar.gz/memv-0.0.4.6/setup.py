
from setuptools import setup, find_packages

setup(
    name='memv',
    version='0.0.4.6',
    description='Create graph to visualize memory usage',
    author='nhunh',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'numpy',
        'psutil',
        'setuptools',
    ],
    entry_points={
        'console_scripts': [
            'memv=memv.memv:memv',
        ],
    },
)