try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from tessti import __author__, __email__, __version__


name = "tessti"
url = f"https://github.com/ListIndexOutOfRange/{name}"

with open("README.md", "r") as f:
    readme = f.read()

install_requires = ["toml",]

setup(
    name=name,
    version=__version__,
    description="A tool to schedule SLURM jobs made as simple as possible.",
    long_description_content_type="text/markdown",
    long_description=readme,
    author=__author__,
    author_email=__email__,
    url=url,
    packages=["tessti", ],
    package_dir={"tessti": "tessti"},
    install_requires=install_requires,
    license="GPLv3",
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
)


# _______________________________________________________________________________________________ #
# Using this script:
# >>> python setup.py sdist bdist_wheel

# Resulting package should be inspected, checked, and tested with:
# > twine check dist/*
# > twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Then finally if everything is ok:
# twine upload dist/*
# _______________________________________________________________________________________________ #
