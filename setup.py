from setuptools import setup

setup(
    name='testclick',
    version='0.1.0',
    py_modules=['testclick'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'testclick = testclick:dots',
        ],
    },
)