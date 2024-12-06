from setuptools import setup, find_packages

setup(
    name='ezpath',
    version='1.1',
    packages=find_packages(),
    description='Turn-Key solution to manage paths relative to the current file',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Vittorio Pascucci',
    py_modules=['ezpath'],
    python_requires='>=3.6',
    install_requires=[],
)
