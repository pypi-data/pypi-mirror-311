from setuptools import Extension, setup


setup(ext_modules=[Extension('cgeo._cgeo', ['cgeo.c'])])
