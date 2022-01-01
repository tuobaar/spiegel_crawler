# Spiegel International Web Crawler

This program crawls news-entries from the URL https://www.spiegel.de/international/ and stores it in a sqlite database every 15 minutes.


## Technologies and modules:

- python3
- sqlite3
- sys
- signal
- time
- datetime
- requests
- bs4 (beautifulsoup4)
- pandas

Some modules are already part of the python install package. Other modules can be installed through pip install 'module name'.


## Program features:

1. Crawls url every 15 minutes.
2. Crawls multiple pages if instructed by user.
3. Handle requests errors.
4. Handles internet/network connection errors. The program keeps running waiting for the
   connection to get fixed, and continues afterwards.
5. Handles duplicate entries.
6. Handles missing data.
7. Program informs the user about changes in HTML tags and CSS classes on the URL/Webpage.
8. On program termination, the first 5 latest new-entries are displayed.


## Installation:
1. Click on the [Code](https://github.com/tuobaar/spiegel_crawler/archive/refs/heads/main.zip) button on main project page on GitHub and download zip file.
2. Extract the downloaded zip file to a preferred location on your computer.
3. Open command console/prompt within the extracted folder and pip install modules.txt as:

   `>>> pip install --requirements modules.txt`

## How to use
1. The program can be launched by entering the following in a command console/prompt:

   `>>> python spiegel_crawler.py`  
   `>>> python3 spiegel_crawler.py`

2. To view a dataframe of the database, run:

   `>>> python view_database.py`  
   `>>> python3 view_database.py`
