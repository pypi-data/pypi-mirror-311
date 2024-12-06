from setuptools import setup, find_packages

VERSION = '0.0.3-0002'
DESCRIPTION = 'PySpiro'
LONG_DESCRIPTION = 'Spirometry reference correction'

setup(
        name="PySpiro",
        version=VERSION,
        author="Roman Martin, Hendrik Pott",
        author_email="<roman.martin@hhu.de>, <hendrik.pott@uni-marburg.de>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["pandas", "numpy"],

        keywords=['python', 'respirology', 'spirometry'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
