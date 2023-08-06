
from setuptools import setup, find_packages

setup(
    name='memv',
    version='0.0.2.7',
    description='Create graph to visualize memory usage',
    author='nhunh',
    packages=find_packages(),
    install_requires=[
        'matplotlib==2.2.5',
        'numpy==1.22.0',
        'psutil==5.9.0',
        'setuptools==67.8.0',
    ],
    entry_points={
        'console_scripts': [
            'memv=memv.memv:memv',
        ],
    },
)