#compilar con: python setup.py build_ext --inplace

import os
from setuptools import Extension, setup

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
# print(SOURCE_DIR)
# Define the extension module
array = Extension("Array",
                          sources=[os.path.join(SOURCE_DIR, "Array.c")])

# Define the setup parameters
setup(
    name="PackageName",
    version="1.0",
    description="Array implementation for python",
    ext_modules=[array],
)