import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="JulianPy",
    version="1.0.0",
    author="Siddhu",
    author_email="siddhu.pendyala@outlook.com",
    description="Julian Date functionality in python",
    long_description=long_description, # don't touch this, this is your README.md
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [],
    python_requires='>=3.6',
)