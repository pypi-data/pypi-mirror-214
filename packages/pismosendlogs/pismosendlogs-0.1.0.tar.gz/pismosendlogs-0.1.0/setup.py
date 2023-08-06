from setuptools import setup

setup(
    name='pismosendlogs',
    version='0.1.0',    
    description='A library to send logs',
    url='https://github.com/pismo/datalake-jobs',
    author='Pismo Data Team',
    author_email='datalake@pismo.io',
    license='BSD 2-clause',
    packages=['pismosendlogs'],
    install_requires=['boto3',
                      'uuid',
                      'datetime',                   
                      ],

    classifiers=[
    ],
)