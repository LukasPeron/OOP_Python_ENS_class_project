from distutils.core import setup

__version__ = "1.0"

long_description="""Developed by Lukas Péron.
This package is made to implement Feynman diagrams easily in python. There is two main goals to this package.
1st : create and display a diagram using tikz-feynman LaTeX package
2nd : display the integral corresponding to a diagram
python package require : pylatex, pdf2image, IPython
LaTeX package require : tikz-feynman, slashed
!!! ATTENTION THE COMPILATION OF THE .TEX FILE IS DONE WITH LUALATEX !!!
Last update : 22/05/2023
"""

setup(name='feynman_package',
      version=__version__,
      description='De la physique en nombres',
      author='Lukas Péron',
      author_email='lukas.peron@ens.psl.eu',
      url='',
      packages=['feynman_package'],
     )