import mysql.connector
import requests
from mysql.connector import Error, MySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection
from requests import Timeout, TooManyRedirects, HTTPError, RequestException

from config import *
from typing import Any, List, Optional, Tuple, Union

from utils import sbyPrint, countdown


def connect_db() -> Union[PooledMySQLConnection, MySQLConnectionAbstract, None]:
    """
    Create a database connection using credentials from an environment or config file.

    Tries to establish a connection to the MySQL database with specified credentials.
    If the connection is successful, it logs the server version and the currently
    connected database. If the connection fails, it logs the error encountered.

    Returns:
        PooledMySQLConnection | MySQLConnectionAbstract | None: Returns a database connection object if successful,
        or None if the connection could not be established.

    Usage:
        connection = connect_db()
        if connection:
            # Proceed with database operations
        else:
            # Handle connection failure
    """
    try:
        connection = mysql.connector.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            sbyPrint(f"{{green}}Connected to MySQL Server version {db_info}")
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            sbyPrint(f"{{cyan}}You're connected to database: {record}")
            return connection
    except Error as e:
        sbyPrint(f"{{red}}Error while connecting to MySQL {str(e)}")
        return None


def execute_sql_query(
        connection: Optional[MySQLConnection],
        query: str,
        params: Optional[Tuple[Any, ...]] = None,
        fetch: bool = False
) -> Optional[List[Tuple[Any, ...]]]:
    """
    Execute an SQL query with optional parameters and possibly fetch results.

    Args:
        connection: The database connection object.
        query: A string containing the SQL query to be executed.
        params: A tuple containing parameters to substitute into the SQL query.
        fetch: A boolean indicating whether to fetch the results.

    Returns:
        If fetch is True, returns the fetched results. None is returned if no results
        need to be fetched, or if an error occurs or there is no connection.

    Raises:
        Logs errors related to SQL execution and rolls back transactions in case of failure.
    """
    if connection is None:
        sbyPrint("{red}No connection to the database available.")
        return None

    sbyPrint("{yellow}Starting to execute query.")
    cursor = None
    try:
        cursor = connection.cursor()
        sbyPrint(f"{{blue}}Cursor opened. Executing query: {{magenta}}{query}")

        if params:
            sbyPrint(f"{{magenta}}With parameters: {params}")
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        sbyPrint("{green}Query execution complete.")

        if fetch:
            sbyPrint("{cyan}Fetching results...")
            result = cursor.fetchall()
            sbyPrint("{green}Results fetched successfully.")
            return result
        else:
            sbyPrint("{yellow}Committing transaction...")
            connection.commit()
            sbyPrint("{green}Transaction committed.")
    except Error as e:
        sbyPrint(f"{{red}}An error occurred: {e}")
        sbyPrint("{red}Rolling back transaction...")
        connection.rollback()
    finally:
        if cursor:
            sbyPrint("{blue}Closing cursor.")
            cursor.close()
            sbyPrint("{blue}Cursor closed.")


def make_request(url: str,
                 method: str = 'GET',
                 headers: dict = None,
                 params: dict = None,
                 data: dict = None,
                 timeout: int = 10):
    """
    Sends an HTTP request and handles common HTTP errors.

    Args:
        url (str): The URL to which the request is to be sent.
        method (str): HTTP method, e.g., 'GET', 'POST', etc.
        headers (dict): Optional HTTP headers to send with the request.
        params (dict): URL parameters to append to the URL.
        data (dict): Data to send in the body of the request.
        timeout (int): How many seconds to wait for the server to send data before giving up.

    Returns:
        A requests.Response object if the request was successful.

    Raises:
        Exception: If an HTTP error occurs or other request issues are encountered.
    """
    response = None  # Initialize response to None

    try:
        response = requests.request(method, url, headers=headers, params=params, data=data, timeout=timeout)
        response.raise_for_status()  # Raise HTTPError for bad requests (4XX or 5XX)
    except HTTPError as http_err:
        if response and response.status_code == 401:
            raise Exception("HTTP Error: Unauthorized. Check your API key or authentication details.")
        elif response and response.status_code == 429:
            wait_time = int(response.headers.get("Retry-After", 60))  # Default wait time to 60 seconds if not provided
            sbyPrint(f"{{red}}Rate limit exceeded. Waiting for {{cyan}}{wait_time}{{red}} seconds to retry...")
            countdown(wait_time)
            return make_request(url, method, headers, params, data, timeout)  # Recursive call after waiting
        else:
            raise Exception(f"HTTP Error occurred: {http_err} without a valid response.")
    except (Timeout, TooManyRedirects) as conn_err:
        raise Exception(f"Connection error occurred: {conn_err}")
    except RequestException as req_err:
        raise Exception(f"An error occurred during the request: {req_err}")
    else:
        return response


url = "https://api.coingecko.com/api/v3/coins/list"
response = make_request(url,headers=headers)
print(response.text)