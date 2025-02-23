from distutils.core import setup
from Cython.Build import cythonize

setup(name='intelligence6',
      ext_modules=cythonize("intelligence6.pyx"))
