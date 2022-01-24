import sqlite3


def create_database():
    """
    This function creates a new database with table 'news_archive' if it does not exist in the program directory.

    :return: This function returns no value.
    """
    db_name = 'news_archive.db'

    # Connect to the given database db_name if it exists else create an instance with the same name.

    try:
        # Establish a connection with database db_name

        connection = sqlite3.connect(db_name)

        # Create a cursor object to create table and columns

        my_cursor = connection.cursor()

        create_table = """CREATE TABLE IF NOT EXISTS news_archive (
                                            Title TEXT UNIQUE, 
                                            Sub_Title TEXT, 
                                            Abstract TEXT, 
                                            Download_Time DATETIME, 
                                            Update_Time DATETIME, 
                                            UNIQUE (Title) ON CONFLICT IGNORE
                                            ); """

        my_cursor.execute(create_table)
        my_cursor.close()
        connection.close()

    except sqlite3.Error as error:
        print(f'Error connecting to the database {db_name}', error)

    finally:
        print("\nPreparing to crawl 'https://www.spiegel.de/international/' ")
        print(f'\nConnection to the database {db_name} successful.\n')


def insert_update_database(title, sub_title, abstract, download_time, update_time):
    """
    This function inserts/updates crawled information to the database db_name.
    It takes five parameters, title, sub_title, abstract, download_time and update_time.

    :param title: stores the title information of crawled news data.
    :param sub_title: stores the sub_title information of crawled news data.
    :param abstract: stores the abstract information of crawled news data.
    :param download_time: stores the download timestamp of crawled news data.
    :param update_time: stores the update timestamp of crawled news data.

    :return: This function returns no value.

    """

    db_name = 'news_archive.db'

    try:
        # Establish a connection with database db_name

        connection = sqlite3.connect(db_name)

        # Create a cursor object to insert data into the database

        my_cursor = connection.cursor()

        sqlite_insert_news_data = """INSERT OR IGNORE INTO news_archive (Title, Sub_Title, Abstract, Download_Time,
        Update_Time) VALUES (?, ?, ?, ?, ?) ON CONFLICT (Title) DO UPDATE SET Abstract = EXCLUDED.Abstract, 
        Update_Time = EXCLUDED.Update_Time"""

        my_cursor.execute(sqlite_insert_news_data, (title, sub_title, abstract, download_time, update_time))
        connection.commit()
        my_cursor.close()
        connection.close()

    except sqlite3.Error as error:
        print('Failed to insert/update sqlite table', error)


def display_latest_entries():
    """
    This function displays the first 5 latest news-entries in the database.

    :return: This function returns no value.
    """

    db_name = 'news_archive.db'

    try:
        # Establish a connection with database db_name

        connection = sqlite3.connect(db_name)

        # Create a cursor object to select records from the database

        my_cursor = connection.cursor()

        # Printing the last 5 rows from 'news_archive.db' database
        rows = my_cursor.execute("SELECT * FROM news_archive;").fetchall()
        print("\n\nThe latest news-entries are: \n")
        for row in rows[-5:]:
            print(row, "\n")

        my_cursor.close()
        connection.close()

    except sqlite3.Error as error:
        print('Failed to display sqlite table', error)
