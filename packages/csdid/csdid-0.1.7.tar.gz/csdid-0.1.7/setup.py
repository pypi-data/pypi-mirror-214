from setuptools import setup, find_packages

import os

path = 'dist'
files = os.listdir(path)

for file in files:
  pth = os.path.join(path, file)
  os.remove(pth)

setup(
  name = 'csdid',
  version='0.1.7',
  url='https://github.com/d2cml-ai/csdid',
  author='D2CML Team, Alexander Quispe, Carlos Guevara, Jhon Flroes',
  keywords=['Causal inference', 'Research'],
  license="MIT",
  description='Difference in Difference in Python',
  classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Scientific/Engineering",
    ],
  packages=find_packages(),
  package_data={
    'data': ['data/*'],
    'configs': ['configs/*']
  }
)