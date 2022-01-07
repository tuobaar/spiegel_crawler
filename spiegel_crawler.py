import sys
import signal
import time
from database_tools import create_database, display_latest_entries
from crawl_parse_tools import caption_crawler, middle_crawler, alle_beitraege_crawler


def keyboard_interrupt_handler(signal, frame):
    """
    This function handles KeyboardInterrupt errors and terminates the program.
    """
    print('\n\nTerminating program ...')
    time.sleep(1)
    display_latest_entries()
    print('\n\nProgram terminated.\n')
    sys.exit(0)


signal.signal(signal.SIGINT, keyboard_interrupt_handler)


def spiegel_crawler():
    """
    This is the main function that crawls the URL.
    It makes calls to three other functions  alle_beitraege_crawler(), middle_crawler() and caption_crawler() that crawl
    the needed information.
    """
    print('\rData crawling in session.                                                          ', end='', flush=True)
    time.sleep(3)
    alle_beitraege_crawler(1)
    middle_crawler()
    caption_crawler()
    print("\r", end='', flush=True)
    print('\rSuccessfully inserted/updated new-entries to the database.                         ', end='', flush=True)
    time.sleep(3)
    print("\r", end='', flush=True)


create_database()


# Providing options to crawl either page 1 only or all 500 pages of the URL

prompt = "\nDo you want to crawl all 500 pages? This would usually take about 25 minutes to complete.\n\nAfterwards " \
         "the program will keep crawling page 1 every 15 minutes. "
prompt += "\n\nPlease enter 'y' to proceed or 'n' to crawl only page 1: "

while True:
    message = input(prompt)
    if message == 'y':
        print()
        for page_number in range(500, 0, -1):
            time.sleep(1)
            alle_beitraege_crawler(page_number)
            print(f'\rDone crawling https://www.spiegel.de/international/p{page_number}/. '
                  f'Page index = {page_number}  ', end='', flush=True)
        middle_crawler()
        caption_crawler()
        print()
        break

    elif message == 'n':
        print()
        print("\rAlright. Crawling page 1 now and will keep crawling page 1 every 15 minutes ...", end='', flush=True)
        time.sleep(5)
        print("\r                                                                                 ", end='', flush=True)
        break

    else:
        print()
        print("\rInvalid input. Characters allowed are 'y' and 'n'. Looping back to user input ...", end='', flush=True)
        time.sleep(5)
        print("\r                                                                                 ", end='', flush=True)
        continue

print('\nInserting/updating news-entries into the database every 15 minutes.\n')


# Automatically run the main crawler every 15 minutes

while True:
    spiegel_crawler()
    time.sleep(1)

    # Imitating a countdown timer to show program activity.
    for x in range(898, -1, -1):
        time.sleep(1)
        print(f'\rWaiting to crawl data in the next 15 minutes. Working ... {x} '
              f'seconds remaining', end='', flush=True)
