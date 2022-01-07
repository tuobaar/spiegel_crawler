import datetime
import requests
import time
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.exceptions import SSLError
from requests.packages.urllib3.util.retry import Retry
from database_tools import insert_update_database


def requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_force_list=(429, 500, 502, 503, 504),
        # method_whitelist=("HEAD", "GET", "PUT", "POST", "DELETE", "OPTIONS", "TRACE")
        # allowed_methods=("HEAD", "GET", "PUT", "POST", "DELETE", "OPTIONS", "TRACE")
        session=None,
):
    """
    This function handles subtle irregularities when making requests to the URL.
    It retries requests to the URL.
    """
    session = session or requests.Session()
    retry_strategy = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_force_list,
        # method_whitelist= method_whitelist,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def caption_crawler():
    """
    This function crawls latest news-entries from the URL 'https://www.spiegel.de/international/'.
    It calls the function insert_update_database(title, sub_title, abstract, download_time, update_time) which
    then inserts the crawled information into the database.

    :return: This function returns no value.
    """

    url = 'https://www.spiegel.de/international/'
    headers = {"user-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/96.0.4664.45 Safari/537.36'}

    # Handling request errors, connection errors or network disconnections.

    source_code = ''

    while source_code == '':
        try:
            source_code = requests_retry_session().get(url, headers=headers, timeout=5)

        except SSLError:
            source_code = requests_retry_session().get(url, headers=headers, verify=False, timeout=5)

        except requests.exceptions.ConnectionError:
            print('\rConnection error. Connection to server denied or network problem.            ', end='', flush=True)
            time.sleep(3)
            print("\r", end='', flush=True)
            print('\rPlease check internet/network connection.                                    ', end='', flush=True)
            time.sleep(3)
            print("\r", end='', flush=True)
            print('\rIn the meantime, will keep trying until connection is established. Trying ...', end='', flush=True)
            time.sleep(3)
            print("\r", end='', flush=True)
            continue

    # print(f'Status code: {source_code.status_code}\n')

    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    tit = "align-middle hover:opacity-moderate focus:opacity-moderate"
    sub_tit = "block text-primary-base dark:text-dm-primary-base hover:text-primary-dark focus:text-primary-darker " \
              "font-brandUI font-extrabold lg:text-xl md:text-xl sm:text-l leading-tight mb-8"
    abt = "font-serifUI font-normal lg:text-l md:text-base sm:text-base leading-loose mr-6"

    items = soup.find_all("a", class_="text-black dark:text-shade-lightest block")

    title_news, sub_title_news, abstract_news = [], [], []

    for item in items:
        title_items = item.find_all('span', class_=tit)
        sub_title_items = item.find_all('span', class_=sub_tit)
        abstract_items = item.find_all('span', class_=abt)

        # Fetching elements for the Title column in the database
        for element in title_items:
            title_elements = element.text.strip()
            title_news.append(title_elements)

        # Fetching elements for the Sub_Title column in the database
        for element in sub_title_items:
            sub_title_elements = element.text.strip()
            sub_title_news.append(sub_title_elements)

        # Fetching elements for the Abstract column in the database
        for element in abstract_items:
            abstract_elements = element.text.strip()
            abstract_news.append(abstract_elements)

    # Checking for equal lengths of the lists title_news, sub_title_news and abstract_news to ensure accurate data entry

    length = len(title_news)

    if any(len(item) != length for item in [sub_title_news, abstract_news]):
        print("\n\nAttention! Something went wrong in caption_crawler().")
        print(f'\nThe lengths of the lists title_news, sub_title_news and abstract_news are {len(title_news)}, '
              f'{len(sub_title_news)}, {len(abstract_news)} respectively.')
        print("The unequal values above suggests that something went wrong. \nIt's likely that the HTML tags or CSS "
              "classes have changed on the webpage.")
        print('The program will terminate soon to prevent incomplete/incorrect data entries.')
        print('Please contact tech support, fix the issue and run the program again.\n\nTerminating the program'
              ' in a few seconds ... ')
        time.sleep(20)
        raise SystemExit('\nProgram terminated due to a possible change in HTML tags or CSS classes.')
    else:
        for data in zip(reversed(title_news), reversed(sub_title_news), reversed(abstract_news)):
            title = data[0]
            sub_title = data[1]
            abstract = data[2]

            download_time = datetime.datetime.now()
            update_time = datetime.datetime.now()
            insert_update_database(title, sub_title, abstract, download_time, update_time)


def middle_crawler():
    """
    This function crawls older news-entries from the middle section of the URL 'https://www.spiegel.de/international/'.
    It calls the function insert_update_database(title, sub_title, abstract, download_time, update_time) which
    then inserts the crawled information into the database.

    :return: This function returns no value.
    """

    url = 'https://www.spiegel.de/international/'
    headers = {"user-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/96.0.4664.45 Safari/537.36'}

    # Handling request errors, connection errors or network disconnections.

    source_code = ''

    while source_code == '':
        try:
            source_code = requests_retry_session().get(url, headers=headers, timeout=5)

        except SSLError:
            source_code = requests_retry_session().get(url, headers=headers, verify=False, timeout=5)

        except requests.exceptions.ConnectionError:
            print('\rConnection error. Connection to server denied or network problem.            ', end='',
                  flush=True)
            time.sleep(3)
            print("\r", end='', flush=True)
            print('\rPlease check internet/network connection.                                    ', end='',
                  flush=True)
            time.sleep(3)
            print("\r", end='', flush=True)
            print('\rIn the meantime, will keep trying until connection is established. Trying ...', end='',
                  flush=True)
            time.sleep(3)
            print("\r", end='', flush=True)
            continue

    # print(f'Status code: {source_code.status_code}\n')

    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    tit = "hover:opacity-moderate focus:opacity-moderate sm:hyphens-auto"
    tit_faq = "hover:opacity-moderate focus:opacity-moderate"
    sub_tit = "block text-primary-base dark:text-dm-primary-base focus:text-primary-darker hover:text-primary-dark " \
              "font-sansUI font-bold text-base"
    sub_tit_faq = "hover:text-primary-dark focus:text-primary-darker text-primary-base dark:text-dm-primary-base" \
                  " font-sansUI font-bold text-base"

    abt = "font-serifUI font-normal text-base leading-loose mr-6"

    items = soup.find_all(
        'div',
        class_=lambda value: value and value.startswith(("z-10 lg:w-4/12 md:w-6/12", "z-10 lg:w-8/12 md:w-full")))

    for item in reversed(items):

        # Fetching elements for the Title column in the database

        title_item = item.find('span', class_=['align-middle', tit, tit_faq])
        if title_item is None:
            print("\nAttention! Something went wrong for Title entries in middle_crawler().It's likely that the HTML "
                  "tags or CSS classes have changed on the webpage.")
            print('The program will terminate soon to prevent incomplete/incorrect data entries.')
            print('Please contact tech support, fix the issue and run the program again. Terminating the program in a '
                  'few seconds ... ')
            time.sleep(20)
            raise SystemExit('\nProgram terminated due to a possible change in HTML tags or CSS classes.')
        else:
            title = title_item.get_text(strip=True)

        # Fetching elements for the Sub_Title column in the database

        sub_title_item = item.find('span', class_=[sub_tit, sub_tit_faq])
        if sub_title_item is None:
            sub_title = 'Subtitle not available'
        elif sub_title_item.get_text() == '':
            sub_title = 'Subtitle not available'
        else:
            sub_title = sub_title_item.get_text(strip=True)

        # Fetching elements for the Abstract column in the database

        abstract_item = item.find('span', class_=abt)
        if abstract_item is None:
            abstract = 'Abstract not available'
        elif abstract_item.get_text() == '':
            abstract = 'Abstract not available'
        else:
            abstract = abstract_item.get_text(strip=True)

        download_time = datetime.datetime.now()
        update_time = datetime.datetime.now()
        insert_update_database(title, sub_title, abstract, download_time, update_time)


def alle_beitraege_crawler(page_number):
    """
    This function crawls much older news-entries from the URL 'https://www.spiegel.de/international/p{page_number}/'.
    It calls the function insert_update_database(title, sub_title, abstract, download_time, update_time) which
    then inserts the crawled information into the database.

    :return: This function returns no value.
    """

    url = f'https://www.spiegel.de/international/p{page_number}/'
    headers = {"user-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/96.0.4664.45 Safari/537.36'}

    # Handling request errors, connection errors or network disconnections.

    source_code = ''

    while source_code == '':
        try:
            source_code = requests_retry_session().get(url, headers=headers, timeout=5)

        except SSLError:
            source_code = requests_retry_session().get(url, headers=headers, verify=False, timeout=5)

        except requests.exceptions.ConnectionError:
            print('\rConnection error. Connection to server denied or network problem.            ', end='', flush=True)
            time.sleep(3)
            print("\r", end='', flush=True)
            print('\rPlease check internet/network connection.                                    ', end='', flush=True)
            time.sleep(3)
            print("\r", end='', flush=True)
            print('\rIn the meantime, will keep trying until connection is established. Trying ...', end='', flush=True)
            time.sleep(3)
            print("\r", end='', flush=True)
            continue

    # print(f'Status code: {source_code.status_code}\n')

    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    tit = "block font-sansUI font-bold text-xl mb-12"
    sub_tit = "block text-primary-base dark:text-dm-primary-base focus:text-primary-darker hover:text-primary-dark " \
              "font-sansUI font-bold text-base"
    abt = "font-serifUI font-normal text-base leading-loose mr-6"

    items = soup.find_all('section', class_="z-10 w-full")

    for item in items:
        elements = item.find_all('div', class_="lg:w-8/12 md:w-6/12 lg:pl-24 md:pl-24 sm:mx-16")

        for element in reversed(elements):

            # Fetching elements for the Title column in the database

            title_item = element.find('span', class_=tit)
            if title_item is None:
                print(f"\n\nAttention! Something went wrong for Title entries in alle_beitraege_crawler({page_number})."
                      f"\nIt's likely that the HTML tags or CSS classes have changed on the webpage.")
                print('The program will terminate soon to prevent incomplete/incorrect data entries.')
                print('Please contact tech support, fix the issue and run the program again.\n\nTerminating the program'
                      ' in a few seconds ... ')
                time.sleep(20)
                raise SystemExit('\nProgram terminated due to a possible change in HTML tags or CSS classes.')
            else:
                title = title_item.get_text(strip=True)

            # Fetching elements for the Sub_Title column in the database

            sub_title_item = element.find('span', class_=sub_tit)
            if sub_title_item is None:
                sub_title = 'Subtitle not available'
            elif sub_title_item.get_text() == '':
                sub_title = 'Subtitle not available'
            else:
                sub_title = sub_title_item.get_text(strip=True)

            # Fetching elements for the Abstract column in the database

            abstract_item = element.find('span', class_=abt)
            if abstract_item is None:
                abstract = 'Abstract not available'
            elif abstract_item.get_text() == '':
                abstract = 'Abstract not available'
            else:
                abstract = abstract_item.get_text(strip=True)

            download_time = datetime.datetime.now()
            update_time = datetime.datetime.now()
            insert_update_database(title, sub_title, abstract, download_time, update_time)
