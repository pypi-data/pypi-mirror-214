import os.path
import re

from setuptools import find_packages, setup


def parse_version():
    # single source of truth for package version
    version_string = ""
    version_pattern = re.compile(r'__version__ = "([^"]*)"')
    with open(os.path.join("src", "globus_sdk", "version.py")) as f:
        for line in f:
            match = version_pattern.match(line)
            if match:
                version_string = match.group(1)
                break
    if not version_string:
        raise RuntimeError("Failed to parse version information")
    return version_string


def read_readme():
    with open("README.rst") as fp:
        return fp.read()


setup(
    name="globus-sdk",
    version=parse_version(),
    description="Globus SDK for Python",
    long_description=read_readme(),
    author="Globus Team",
    author_email="support@globus.org",
    url="https://github.com/globus/globus-sdk-python",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"globus_sdk": ["py.typed"]},
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.19.1,<3.0.0",
        "pyjwt[crypto]>=2.0.0,<3.0.0",
        # cryptography 3.4.0 is known-bugged, see:
        #   https://github.com/pyca/cryptography/issues/5756
        #
        # pyjwt requires cryptography>=3.3.1,
        # so there's no point in setting a lower bound than that
        #
        # as of 2021-10-13, we have removed the upper-bound, on the grounds that
        # - we actively test on the latest versions
        # - cryptography has a strong API stability policy that makes most releases
        #   non-breaking for our usages
        # - other packages /consumers can specify stricter bounds if necessary
        "cryptography>=3.3.1,!=3.4.0",
        # depend on the latest version of typing-extensions on python versions which do
        # not have all of the typing features we use
        'typing_extensions>=4.0;python_version<"3.10"',
    ],
    # vestigial extras, remove in a future version
    extras_require={"dev": []},
    keywords=["globus"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
