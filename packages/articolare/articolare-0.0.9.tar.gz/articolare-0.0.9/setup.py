from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="articolare",
    version="0.0.9",
    author="Murilo Silvestre",
    description="Python client for the Articolare API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "requests",
        "certifi==2023.5.7",
        "charset-normalizer==3.1.0",
        "exceptiongroup==1.1.1",
        "idna==3.4",
        "iniconfig==2.0.0",
        "packaging==23.1",
        "pluggy==1.0.0",
        "requests==2.31.0",
        "tomli==2.0.1",
        "urllib3==2.0.3"
    ],
    extras_require={
        "dev": [
            "pytest>=3.7",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires='>=3.6',
    license_files = ("LICENSE",),
)
