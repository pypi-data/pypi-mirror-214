from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A basic hello package'
LONG_DESCRIPTION = 'A basic hello package long desc.'

# Setting up
setup(
    name="taibun",
    version=VERSION,
    author="Andrei Harbachov",
    author_email="<andrei.harbachov@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)