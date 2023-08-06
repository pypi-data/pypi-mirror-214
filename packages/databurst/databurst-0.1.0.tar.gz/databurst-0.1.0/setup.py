from setuptools import setup, find_packages

setup(
    name='databurst',
    version='0.1.0',
    author='Elias Mathisen',
    description='Databurst is a Python package for generating random data such as names, addresses, phone numbers, and email addresses. It utilizes external APIs to retrieve realistic and randomized data for testing purposes.',
    long_description='Databurst is a Python package that provides a simple and convenient way to generate random data for testing and development purposes. It includes functions to generate random names, addresses, phone numbers, and email addresses. The package leverages external APIs to fetch realistic and randomized data, ensuring the generated data is diverse and representative. Databurst is designed to be easy to use, making it ideal for generating sample data or populating test databases.',
    url='https://github.com/Elias-mathisen/databurst',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)