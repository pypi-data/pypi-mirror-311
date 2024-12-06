from setuptools import setup, find_packages

VERSION = '0.1.0-01'
DESCRIPTION = 'PySpiro'
LONG_DESCRIPTION = 'Spirometry reference correction'

setup(
        name="PySpiro",
        version=VERSION,
        author="Roman Martin, Hendrik Pott",
        author_email="roman.martin@hhu.de, hendrik.pott@uni-marburg.de",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        package_data={'': ['data/gli_2012_splines.csv', 'gli_2012_coefficients.csv']},
        include_package_data=True,
        install_requires=["pandas", "numpy"],
        keywords=['python', 'respirology', 'spirometry'],
        classifiers= [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Healthcare Industry",
            "Intended Audience :: Science/Research",
            "Intended Audience :: Education",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Operating System :: MacOS",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: Unix",
        ]
)
