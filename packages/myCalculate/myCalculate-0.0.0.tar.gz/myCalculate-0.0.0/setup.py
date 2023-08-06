from setuptools import setup, find_packages

VERSION = '' 
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'This Python module serve as a calculator. Am just implementing my skills on paging your module to pypi.'

# Setting up
setup(
       # the name must match the folder name in my own case 'myCalculate'
        name="myCalculate",
        version=VERSION,
        author="Godspower Maurice",
        author_email="verbosetwomillion@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)