from setuptools import find_packages, setup

setup(
    name='efsspysdk',
    version='0.0.2',
    author='Emmanuel Felipe Silva Santos',
    author_email='hi@emmanuel.cloud',
    description='A SDK for the-one-api.dev API',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*', 'tests.*']),    
    install_requires=['pytest', 'requests'],
    license='MIT',
)