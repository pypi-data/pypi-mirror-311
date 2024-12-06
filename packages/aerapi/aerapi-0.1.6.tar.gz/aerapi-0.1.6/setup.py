from setuptools import setup, find_packages

setup(
    name="aerapi",
    version="0.1.6",
    description="A package for accessing APIs used by the data team",
    author="S. Nicholson",
    author_email="Sean.Nicholson@aerlytix.com",
    url="https://github.com/stelltec/aerapi.git",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  # Specify Markdown for PyPI
    packages=find_packages(),  # Ensure it finds the aerapi folder
    package_dir={"": "."},  # Top-level folder is the root
    install_requires=[
        "requests",
        "PyYAML",
        "jsonschema",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    license="MIT",
)
