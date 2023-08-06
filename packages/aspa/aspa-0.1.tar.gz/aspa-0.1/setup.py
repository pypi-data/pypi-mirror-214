from setuptools import setup

setup(
    name='aspa',
    version='0.1',
    packages=['aspa'],
    entry_points={
        'console_scripts': [
            'aspa=aspa.aspa:main',
        ],
    },
    install_requires=[
        'scapy'
    ],
)
