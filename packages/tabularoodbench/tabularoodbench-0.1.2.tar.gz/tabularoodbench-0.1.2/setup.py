from setuptools import setup,find_packages

setup(
    name='tabularoodbench',
    version='0.1.2',    
    description='A package of several settings of out-of-distributoin generalization problem on tabular data',
    url='https://github.com/LJSthu/TabularOODBenchmark',
    author='Jiashuo Liu, Tianyu Wang, Peng Cui, Hongseok Namkoong',
    author_email='liujiashuo77@gmail.com',
    packages=find_packages(),
    install_requires=['pandas',
                      'numpy',                     
                      'scikit-learn'
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        'Operating System :: POSIX :: Linux',
    ],
    python_requires=">=3",
)