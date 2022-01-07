import sqlite3
import pandas as pd


def view_database():
    """
    This function displays a dataframe of the database.
    """

    db_name = 'news_archive.db'

    try:
        # Establish a connection with database db_name
        connection = sqlite3.connect(db_name)

        # Make query, read and display database
        view = "SELECT * FROM news_archive;"
        df = pd.read_sql_query(view, connection)
        print(df)

        connection.close()

    except sqlite3.Error as error:
        print('Failed to display sqlite database/table', error)


view_database()

