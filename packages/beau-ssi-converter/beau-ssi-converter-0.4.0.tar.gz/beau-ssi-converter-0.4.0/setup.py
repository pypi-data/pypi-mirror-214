import re

from setuptools import setup

def _read_long_description():
    try:
        with open("README.md") as fd:
            return fd.read()
    except Exception:
        return None

with open("converter/__init__.py", "r") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

setup(
    name="beau-ssi-converter",
    version=version,
    url="http://github.com/thuongnn/github-actions-learning-python",
    author="Nguyen Nhu Thuong",
    author_email="thuongnn@ssi.com.vn",
    description="Automatic Semantic Versioning for Python projects",
    long_description=_read_long_description(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)