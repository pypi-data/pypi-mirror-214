from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name="getaltbranches",
    version="0.1.0",
    author="Alexander Seropyan",
    author_email="aliksandrion@gmail.com",
    description="A lightweight library for getting branches from public REST API",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/aliksandrion/get_alt_branch",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
