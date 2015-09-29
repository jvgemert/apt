from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'slink app',
  ext_modules = cythonize("slink.pyx"),
)
