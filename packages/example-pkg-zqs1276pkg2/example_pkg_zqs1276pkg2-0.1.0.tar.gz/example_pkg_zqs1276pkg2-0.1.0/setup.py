# setup.py

from setuptools import setup, find_packages

setup(
    name="example-pkg-zqs1276pkg2",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "example-pkg-zqs1276pkg1",
    ],
    author="zqs",
    author_email="",
    description="This is the second package that depends on zqs1276pkg1",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url="",
)
