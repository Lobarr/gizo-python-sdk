import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="gizo-sdk",
    version="0.0.1",
    author="Jesuloba Egunjobi",
    author_email="jesulobaegunjobi@hotmail.com",
    url="https://github.com/gizo-network/gizo-python-sdk",
    description="Gizo network python sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
