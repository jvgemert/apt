from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'Intersection over Union for tubes',
  ext_modules = cythonize("tubeIoU.pyx"),
)
