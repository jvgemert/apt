from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'evaluating tubes',
  ext_modules = cythonize("tube2trajIDs.pyx"),
)
