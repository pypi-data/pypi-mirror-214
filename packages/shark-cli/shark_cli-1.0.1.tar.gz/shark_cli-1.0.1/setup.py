from setuptools import setup, find_packages

setup(
    name='shark_cli',
    version='1.0.1',
    description='shark_cli',
    author='taygish',
    author_email='spacedicknew@gmail.com',
    packages=find_packages(),
    install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
)
