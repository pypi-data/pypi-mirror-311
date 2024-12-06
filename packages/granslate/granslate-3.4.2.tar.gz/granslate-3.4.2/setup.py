#!/usr/bin/env python
# -*- coding: utf-8 -*-
import contextlib, os.path, re

from setuptools import find_packages, setup


def get_file(*paths):
    path = os.path.join(*paths)
    with contextlib.suppress(IOError):
        with open(path, "rb") as f:
            return f.read().decode("utf8")


def get_version():
    init_py = get_file(os.path.dirname(__file__), "granslate", "__init__.py")
    pattern = r"{0}\W*=\W*\"([^']+)\"".format("__version__")
    (version,) = re.findall(pattern, init_py)
    return version


def get_description():
    init_py = get_file(os.path.dirname(__file__), "granslate", "__init__.py")
    pattern = r'"""(.*?)"""'
    (description,) = re.findall(pattern, init_py, re.DOTALL)
    return description


with open("README.md", "r") as fp:
    long_description = fp.read()


def install():
    setup(
        name="granslate",
        version=get_version(),
        description=get_description(),
        long_description=long_description,
        license="MIT",
        author="Simone",
        url="https://github.com/adityaprasad502/yafgt",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Education",
            "Intended Audience :: End Users/Desktop",
            "License :: Freeware",
            "Operating System :: POSIX",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: MacOS :: MacOS X",
            "Topic :: Education",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.10",
        ],
        packages=find_packages(exclude=["docs", "tests"]),
        keywords="google translate translator",
        install_requires=[
            "httpx[http2]==0.25.2",
        ],
        tests_require=[
            "pytest",
            "coveralls",
        ],
        scripts=["translate"],
    )


if __name__ == "__main__":
    install()
