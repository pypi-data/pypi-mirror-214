import os 
from setuptools import find_packages, setup

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()

long_description = read_file('README.md')

license = read_file('LICENSE')

setup(
    name='efsspysdk',
    version='0.0.3',
    author='Emmanuel Felipe Silva Santos',
    author_email='hi@emmanuel.cloud',
    description='A SDK for the-one-api.dev API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license=license,
    python_requires='>=3.9',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*', 'tests.*']),    
    install_requires=['pytest', 'requests'],
)