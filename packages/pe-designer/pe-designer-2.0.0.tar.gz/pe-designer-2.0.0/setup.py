import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pe-designer",
    version="2.0.0",
    author="Gue-ho",
    description="Prime editing tools that consist of a reverse transcriptase linked with Cas9 nickase are capable of generating targeted insertions, deletions,and base conversions without producing DNA double strand breaks or requiring any donor DNA.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gue-ho/PE-Designer",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
