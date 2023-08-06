from setuptools import setup, find_packages
# import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()

VERSION = '0.0.7'
DESCRIPTION = 'A simple interpolator.'
# LONG_DESCRIPTION = 'A package that helps to create a bilinear interpolant and visualise it.'

# Setting up
setup(
    name="simple-interpolator",
    version=VERSION,
    author="var-pi (Stefan Ehin)",
    author_email="<stefanehin4@gmail.com>",
    description=DESCRIPTION,
    # long_description_content_type="text/markdown",
    # long_description=long_description,
    packages=find_packages(),
    install_requires=['matplotlib','numpy','functools'],
    keywords=['python', 'interpolation', 'bilinear', 'math', 'graph', '3D'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)