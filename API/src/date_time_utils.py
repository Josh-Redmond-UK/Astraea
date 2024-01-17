from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Tuple

def get_months(start: str, end: str) -> List[Tuple[str, str]]:
    '''Returns a list of tuples of the first and last day of each month between the start and end dates.

    Args:
        start (str): The start date in the format 'dd-mm-yyyy'.
        end (str): The end date in the format 'dd-mm-yyyy'.

    Returns:
        List[Tuple[str, str]]: A list of tuples containing the first and last day of each month between the start and end dates.
    '''

    # Convert the input strings to datetime objects
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')

    # Initialize the list to store the results
    months = []

    # Iterate from start date to end date
    current_date = start_date
    while current_date <= end_date:
        # First day of the month is always 1
        first_day = datetime(current_date.year, current_date.month, 1)

        # Last day of the month is the day before the first day of next month
        last_day = datetime(current_date.year, current_date.month, 1) + relativedelta(months=1) - timedelta(days=1)

        # Append the first and last day of the month to the list
        months.append((first_day.strftime('%Y-%m-%d'), last_day.strftime('%Y-%m-%d')))

        # Move to the first day of the next month
        current_date = first_day + relativedelta(months=1)

    return months

def get_years(start: str, end: str) -> List[Tuple[str, str]]:
    '''Returns a list of tuples of the first and last day of each year between the start and end dates.

    Args:
        start (str): The start date in the format 'dd-mm-yyyy'.
        end (str): The end date in the format 'dd-mm-yyyy'.

    Returns:
        List[Tuple[str, str]]: A list of tuples containing the first and last day of each year between the start and end dates.
    '''

    # Convert the input strings to datetime objects
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')

    # Initialize the list to store the results
    years = []

    # Iterate from start date to end date
    current_date = start_date
    while current_date <= end_date:
        # First day of the year is always January 1st
        first_day = datetime(current_date.year, 1, 1)

        # Last day of the year is December 31st
        last_day = datetime(current_date.year, 12, 31)

        # Append the first and last day of the year to the list
        years.append((first_day.strftime('%Y-%m-%d'), last_day.strftime('%Y-%m-%d')))

        # Move to the first day of the next year
        current_date = first_day + relativedelta(years=1)

    return years
