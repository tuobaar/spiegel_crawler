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

Some modules are already part of the python3 install package. Other modules/packages can be installed through `pip install package_name` or `pip3 install package_name` .

### Database
The sqlite database is created the first time the program is executed and skipped on subsequent program executions.   
The database contains a table 'news_archive.db' with the following columns:   
`Title TEXT UNIQUE, Sub_Title TEXT, Abstract TEXT, Download_Time DATETIME, Update_Time DATETIME` 

## Program features:

1. Crawls url every 15 minutes.
2. Crawls multiple pages if instructed by user. When the program starts, the user is given an option to either crawl all 500 pages of the URL https://www.spiegel.de/international/p{page_number}/ or only page 1 of same URL.
3. Handles requests errors.
4. Handles internet/network disconnection errors during requests to webpages. The program keeps running waiting for the connection to get fixed, and continues afterwards.
5. Handles duplicate entries.
6. Handles missing data.
7. Program informs the user about changes in HTML tags and CSS classes on the URL/Webpage. However this may not happen, as the HTML tags and CSS classes seem permanent and consistent so far.
8. On program termination, the first 5 latest new-entries are displayed.


## Installation:
1. Click on the [Code](https://github.com/tuobaar/spiegel_crawler/archive/refs/heads/main.zip) button on main project page on GitHub and download zip file.
2. Extract the downloaded zip file to a preferred location on your computer.
3. Open command console/prompt within the extracted folder and install all packages in `modules.txt` using pip as follows:

   `>>> pip install --requirements modules.txt`  
   `>>> pip install -r modules.txt`   
   `>>> pip3 install --requirements modules.txt`  
   `>>> pip3 install -r modules.txt`
   

## How to use:
1. The program can be launched by entering the following in a command console/prompt:

   `>>> python spiegel_crawler.py`  
   `>>> python3 spiegel_crawler.py`

2. To view a dataframe of the database, run:

   `>>> python view_database.py`  
   `>>> python3 view_database.py`
