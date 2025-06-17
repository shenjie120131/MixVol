
from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name='mixture_pricing',
    ext_modules=cythonize([
        "mixture/pricing.pyx",
        "mixture/binomial_pricer.pyx"
    ]),
    include_dirs=[numpy.get_include()],
    zip_safe=False,
)
