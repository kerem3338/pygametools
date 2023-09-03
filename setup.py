from setuptools import setup, find_packages

setup(
    name="pygametools",
    version="0.0.1",
    description="",
    author="Kerem ATA",
    author_email="diosyazilim@gmail.com",
    url="",
    license='MIT',
    packages=find_packages(),
    install_requires=['pygame'],
    long_description=open('README.MD', 'r', encoding='utf-8').read(),
)
