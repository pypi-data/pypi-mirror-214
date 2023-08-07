from setuptools import setup, find_packages

setup(
    name="tarshim",
    version="1.0.0",
    author="Boris Gorelik",
    author_email="boris@gorelik.net",
    description="Neat plot handling in python",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bgbg/tarshim",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "jupyter",
        "matplotlib",
        "seaborn",
    ],
)
