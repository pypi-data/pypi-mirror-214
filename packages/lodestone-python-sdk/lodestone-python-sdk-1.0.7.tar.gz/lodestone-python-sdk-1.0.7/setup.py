import pathlib

from setuptools import setup, find_packages

version = '1.0.7'

setup(
    name="lodestone-python-sdk",
    version=version,
    author="bocai",
    author_email="peijianbo@tuyoogame.com",
    description="Auth to tuyoo's Lodestone",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",

    install_requires=['requests', 'urllib3<2.0'],
    packages=find_packages(),

    python_requires='>3.2',
)
