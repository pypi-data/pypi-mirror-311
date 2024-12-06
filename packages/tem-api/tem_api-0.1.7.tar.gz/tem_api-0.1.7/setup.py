from setuptools import find_packages, setup

with open("./README.md") as f:
    readme = f.read()

with open("./LICENSE") as f:
    license = f.read()

extras_test = [
    "ruff==0.7.4",
]

setup(
    name="tem-api",
    keywords=[
        "tem",
        "api",
        "tron",
    ],
    description="Python API lib for TEM (https://tronenergy.market/) ",
    use_scm_version=True,
    long_description=readme,
    long_description_content_type="text/markdown",
    license=license,
    author="Bohdan Kushnir",
    install_requires=[
        "aiohttp>=3.11.2",
        "pydantic>=2.9.2",
    ],
    extras_require={
        "test": extras_test,
    },
    author_email="",
    setup_requires=[
        "setuptools_scm",
    ],
    url="https://github.com/8ByteCore8/tem-api",
    project_urls={
        "Source": "https://github.com/8ByteCore8/tem-api",
    },
    packages=find_packages(exclude=["tests", "examples"]),
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
