"""setup module."""

import re
from distutils.core import setup
from pathlib import Path

from setuptools import find_packages

name = "mse_lib_crypto"

version = re.search(
    r"""(?x)
    __version__
    \s=\s
    \"
    (?P<number>.*)
    \"
    """,
    Path(f"src/{name}/__init__.py").read_text(),
)

setup(
    name=name,
    version=version["number"],
    url="https://cosmian.com",
    license="MIT",
    author="Cosmian Tech",
    author_email="tech@cosmian.com",
    description="Cryptography Library for MicroService Encryption",
    packages=find_packages("src"),
    package_dir={"": "src"},
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    zip_safe=False,
    install_requires=["cryptography>=41.0.1,<42.0.0", "pynacl>=1.5.0,<2.0.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=["wheel"],
    tests_require=["pytest>=7.2.0,<8.0.0"],
    package_data={"mse_lib_crypto": ["py.typed"]},
    include_package_data=True,
)
