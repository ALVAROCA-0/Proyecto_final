#compilar con: python setup.py build_ext --inplace
from distutils import sysconfig
from Cython.Distutils import build_ext
import os
from setuptools import Extension, setup

class NoSuffixBuilder(build_ext):
    def get_ext_filename(self, ext_name):
        filename = super().get_ext_filename(ext_name)
        suffix = sysconfig.get_config_var('EXT_SUFFIX')
        ext = os.path.splitext(filename)[1]
        return filename.replace(suffix, "") + ext

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
# print(SOURCE_DIR)
# Define the extension module
array = Extension("Array",
                          sources=[os.path.join(SOURCE_DIR, "Array.c")])

# Define the setup parameters
setup(
    name="Array",
    version="1.0",
    description="Array implementation for python",
    ext_modules=[array],
    cmdclass={"build_ext": NoSuffixBuilder},
)