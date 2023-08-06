from setuptools import setup, find_packages

VERSION = "0.0.2"
DESCRIPTION = "A package to run sim reconstructions including parameter estimation."
AUTHOR = "Jakob Wessendorf"

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

def get_packages():
    print(find_packages())
    return find_packages()

setup(
    name="pyfairsim",
    version=VERSION, 
    author=AUTHOR,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=get_packages(),
    license="",
    url="",
    install_requires=["numpy", "matplotlib", "scipy"],
    python_requires=">=3",
    keywords=["sim", "reconstruction", "parameter estimation"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
)
#ToDo at some point setup.py should be replaced by pyproject.toml