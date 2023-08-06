import os

from setuptools import setup
package_directory = os.path.dirname(os.path.abspath(__file__))
with open('README.md', 'r') as f:
    long_description = f.read()
setup(
    name='HormuudEVCPlusMerchant',
    version='1.0.6',
    author='Imran Adem',
    description='A Python package for interacting with the HormuudEVCPlusMerchant Payment  ',
    long_description=long_description,  # Set the long description
    long_description_content_type='text/markdown',  # Specify the content type of the long description
    packages=[package_directory],
    install_requires=['requests'],
    url='https://github.com/skydheere/HormuudEVPlusMarchant',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
