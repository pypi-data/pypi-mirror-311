"""Setup script for the Flick Python SDK."""
import os  # Standard library imports
from setuptools import setup, find_packages  # type: ignore


working_directory = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dthriz',
    version='0.0.1',
    author='Qraba inc',
    description='Flick Python SDKs contains FlickPay inflow and outflow solutions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url='https://merchant.getflick.co/',
    author_email='kingsley@getflick.app',
    license='MIT',
    keywords=[
        "flickpaysdk",
        "card",
        "bank",
        "transfer",
        "payout",
        "inflow",
        "outflow",
    ],
    install_requires=[],
)
