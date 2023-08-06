from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.1.1'
DESCRIPTION = 'A simple interpolator.'

# Setting up
setup(
    name="simple-interpolator",
    version=VERSION,
    author="var-pi (Stefan Ehin)",
    author_email="<stefanehin4@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['matplotlib','numpy'],
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