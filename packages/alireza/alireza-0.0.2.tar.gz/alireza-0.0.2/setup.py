from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Useful tools for python frameworks'
LONG_DESCRIPTION = 'The purpose of starting this project is to make useful tools for all Python frameworks and make the life of programmers easier :)'

# Setting up
setup(
    name="alireza",
    version=VERSION,
    author="Alireza Soroush",
    author_email="alirezasoroush@hotmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'tools', 'framework', 'django',],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
