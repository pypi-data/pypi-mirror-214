from setuptools import setup, find_packages

setup(
    name='seff',
    version='1.0',
    packages=find_packages(),
    author="Jerrin Shirks",
    author_email="jerrinshirks@gmail.com",
    url="https://github.com/zugebot/seff",
    description="A compact and efficient binary file serializer and deserializer for Python dictionaries.",
    long_description="""This package provides a high-performance solution to reading and writing Python dictionaries to and from binary files. The main advantage over JSON or other text-based serialization formats is its compactness and speed, which can be a crucial factor when working with large data sets. 

The package provides two main methods, `write` and `read`, to write a Python dictionary or list of dictionaries to a file and read it back. It intelligently manages the type mapping during serialization and deserialization to ensure type consistency.

The `write` method writes a dictionary (or a list of dictionaries) to a binary file. It automatically handles different data types including int, float, and str. The `read` method reads a binary file and reconstructs the dictionary. The package also provides support functions to deal with file operations.

This package is designed to be easy-to-use, lightweight and efficient, and is particularly suitable for applications that require handling large amounts of data or high-speed I/O operations.
"""
)
