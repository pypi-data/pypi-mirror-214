from setuptools import setup, find_packages

setup(
    name='shark_ser',
    version='1.0.1',
    description='shark_ser',
    author='taygish',
    author_email='spasedicknew@gmail.com',
    packages=find_packages(),
    install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
)
