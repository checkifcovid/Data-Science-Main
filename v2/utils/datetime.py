"""These functions are standard as per v2"""

import re
import datetime

# the following functions searches for a datetime in a string
def find_date_in_str(string):
    """
    Returns the date from a given string

    Note: datetime format is either ``%Y-%m-%d` or ``%m-%d-%Y`
    """
    pattern = re.compile(
        "[0-9]{4}-[0-9]{2}-[0-9]{2}" +
        "|" + #Or
        "[0-9]{2}-[0-9]{2}-[0-9]{4}"
    )
    dt = pattern.search(string).group()

    if re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}",dt):
        dt = datetime.datetime.strptime(dt,"%Y-%m-%d")
    else:
        dt = datetime.datetime.strptime(dt,"%m-%d-%Y")
    return dt
