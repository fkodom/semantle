import os
from distutils.core import setup
from subprocess import getoutput

import setuptools


def get_version_tag() -> str:
    try:
        version = os.environ["SEMANTLE_VERSION"]
    except KeyError:
        version = getoutput("git describe --tags --abbrev=0")

    return version


setup(
    name="semantle",
    version=get_version_tag(),
    author="Frank Odom",
    author_email="frank.odom.iii@gmail.com",
    url="https://github.com/fkodom/semantle",
    packages=setuptools.find_packages(exclude=["tests"]),
    description="A minimal Python library for playing and solving 'Nerdle' problems",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["colorama", "gdown"],
    extras_require={"test": ["black", "flake8", "isort", "pytest", "pytest-cov"]},
    entry_points={
        "console_scripts": [
            "play-semantle=semantle.game:main",
            "solve-semantle=semantle.solver:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
