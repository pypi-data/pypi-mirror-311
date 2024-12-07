from setuptools import find_packages, setup

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ehrt",
    packages=find_packages(include=["ehrt"]),
    version="0.1.4",
    description="EHR Processing Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Vidul Ayakulangara Panickan",
    install_requires=["petehr"],
    python_requires=">=3.6",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)
