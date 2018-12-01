from setuptools import setup

setup(
    name='TypeA',
    version='0.2dev',
    packages=['typea',],
    long_description=open('README.md').read(),
    install_requires=[
        "PyPDF2 >= 1.26.0"
    ],
)
