import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_descriptions = fh.read()

setuptools.setup(
    name="bmkgquake",
    version="0.1.1",
    author="Destin Erika Nawang Budiarti",
    author_email="destinerikanb@gmail.com",
    description="This package provides a simple way to retrieve latest earthquake data in Indonesia from the official website of the Indonesian Meteorology, Climatology, and Geophysics Agency (BMKG)",
    long_description=long_descriptions,
    long_description_content_type='text/markdown',
    url="https://github.com/destin-stack/BMKGquake-fetcher-package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)