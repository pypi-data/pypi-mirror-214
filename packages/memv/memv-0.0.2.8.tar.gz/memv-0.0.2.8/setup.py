
from setuptools import setup, find_packages

setup(
    name='memv',
    version='0.0.2.8',
    description='Create graph to visualize memory usage',
    author='nhunh',
    packages=find_packages(),
    install_requires=[
        'matplotlib==2.2.5',
        'numpy==1.16.6',
        'psutil==5.9.0',
        'setuptools==67.8.0',
    ],
    entry_points={
        'console_scripts': [
            'memv=memv.memv:memv',
        ],
    },
)