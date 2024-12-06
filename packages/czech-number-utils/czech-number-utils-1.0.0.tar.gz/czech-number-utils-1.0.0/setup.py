from setuptools import setup, find_packages

setup(
    name="czech-number-utils",
    version="1.0.0",
    description="Convert numbers to Czech text representations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Zbigniew Lipka",
    author_email="z.lipka@seznam.cz",
    url="https://github.com/zbyso23/czech-number-utils",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)