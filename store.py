"""Handles storing and reading from earlier Subreddit Count files."""

import datetime
import os
from typing import Optional, Tuple
import json

os.makedirs('store', exist_ok=True)
STORE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'store')


def store(sub_count_data: dict):
    """
    Stores a dictionary in which Subreddit subscriber count data
    is stored in a new JSON file. The argument `sub_count_date`
    must be a dictionary denoting the Subreddit names and their
    respective subscriber counts in the following format:

        {
            "bardmains": 9000,
            "Rivenmains": 8000,
            "YasuoMains": 7000,
            ...
        }

    Note the case-sensitivity. This is important to display the
    correct images when a table is generated for /r/ChampionMains.
    """

    file_name = os.path.join(STORE_DIR, str(datetime.date.today()))

    with open(file_name + '.json', 'w+') as outfile:
        json.dump(sub_count_data, outfile, sort_keys=True, indent=4)


def newest() -> Optional[Tuple[datetime.date, dict]]:
    """
    Returns the newest file from the store, meaning the latest update.
    In addition to this, it returns the `datetime.date` on which the
    file was written. These values get returned in a tuple.
    The second item in the tuple will be in the format shown above,
    with the exception that the keys will be sorted.

    If no file was found in the directory,
    `None` is returned.
    """

    dir_contents = os.listdir(STORE_DIR)
    if not dir_contents:
        return None

    latest = max(dir_contents)
    date_arr = [int(num) for num in latest.split('-')]
    modification_date = datetime.date(
        year=date_arr[0],
        month=date_arr[1],
        day=date_arr[2]
    )

    with open(os.path.join(STORE_DIR, latest)) as newest_file:
        return modification_date, json.load(newest_file)
