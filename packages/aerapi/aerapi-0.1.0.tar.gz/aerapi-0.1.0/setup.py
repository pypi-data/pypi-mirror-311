from setuptools import setup, find_packages

setup(
    name="aerAPI",
    version="0.1.0",
    description="A package for accessing APIs used by the data team",
    author="S. Nicholson",
    author_email="Sean.Nicholson@aerlytix.com",
    url="https://github.com/stelltec/aerapi.git",
    packages=find_packages(exclude=["tests*", "examples*"]),
    install_requires=[
        "requests",
        "PyYAML"   
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    license="MIT",
)
