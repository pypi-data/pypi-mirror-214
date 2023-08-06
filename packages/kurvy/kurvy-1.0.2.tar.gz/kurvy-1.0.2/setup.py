import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kurvy",
    version="1.0.2",
    author="celerygemini",
    description="Curve approximation toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/celerygemini/kurvy",
    packages=setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
