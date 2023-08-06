import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pedesign",
    version="1.0",
    description="Prime editing tools that consist of a reverse transcriptase linked with Cas9 nickase are capable of generating targeted insertions, deletions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gue-ho/PE-Designer",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
