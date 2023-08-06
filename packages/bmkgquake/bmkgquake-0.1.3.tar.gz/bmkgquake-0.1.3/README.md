# BMKG Quake Package

[![License](https://img.shields.io/badge/license-GNU%20General%20Public%20License%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)
[![Python](https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9-blue)](https://www.python.org)
[![Beautiful Soup](https://img.shields.io/badge/Beautiful%20Soup-4-red)](https://pypi.org/project/beautifulsoup4/)
[![Requests](https://img.shields.io/badge/Requests-2.26.0-red)](https://pypi.org/project/requests/)

This package provides a simple way to retrieve real-time earthquake data in Indonesia from the official website of the Indonesian Meteorology, Climatology, and Geophysics Agency (BMKG). It utilizes web scraping techniques using the `beautifulsoup4` and `requests` packages to fetch earthquake data from the BMKG website. The retrieved data is then returned as a Python dictionary or JSON format, which can be used in web or mobile applications.

## Key Features

- Real-time Data Retrieval: Fetches the latest earthquake data from the BMKG website in real-time.
- Simple Web Scraping: Utilizes `beautifulsoup4` and `requests` packages for efficient web scraping of earthquake data.
- Data Format: Returns earthquake data as a Python dictionary or JSON for easy integration into applications.
- Wide Python Version Support: Compatible with Python 3.6 or later.

## Installation

Install the package using pip:

```bash
pip install bmkgquake
```

## Usage

```bash
import bmkgquake 

result = bmkgquake.extract_data()
bmkgquake.display_data(result)
```



