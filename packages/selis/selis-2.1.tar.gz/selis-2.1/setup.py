from setuptools import setup

setup(
    name='selis',
    version='2.1',
    packages=['selis'],
    entry_points={
        'console_scripts': [
            'selis=selis.selis:main',
        ],
    },
    install_requires=[
        'requests',
    ],
)
