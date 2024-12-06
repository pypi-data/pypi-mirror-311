from setuptools import setup, find_packages

VERSION = '0.0.6' 
DESCRIPTION = 'BinaryClust Python'
LONG_DESCRIPTION = 'Python Reimplementation of the R package BinaryClust'


setup(
        name="pyBinaryClust", 
        version=VERSION,
        author="Desmond Choy",
        author_email="<desmondchoy@cantab.net>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(where='src'),
        package_dir={"": "src"},
        install_requires=["numpy", "scipy", "pandas", "matplotlib", "seaborn", "scikit-learn", "umap"],
        keywords=['python', 'BinaryClust', 'CyTOF', 'bioinformatics', 'cytometry']
)