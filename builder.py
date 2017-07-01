"""Builds tables for use in Reddit."""

import json

import client


def get_sub_info() -> dict:
    """
    Retrieves the Subscriber counts for the
    Subreddits specified in `config.json`
    under the key `subreddits`.

    Returns a dictionary in the format
    {
        'subreddit_name': sub_count,
        ...
    }
    The list is sorted in the order
    in which the subreddits are listed
    in the configuration file.
    """

    with open('config.json') as config:
        subreddits = json.load(config)['subreddits']
    result = {}
    for sub in subreddits:
        sub_info = client.get_sub(sub)
        result[sub_info.display_name] = sub_info.subscribers
    return result


def get_table(sort_by_name: bool = True) -> str:
    """
    Returns a string containing a table in
    Reddit's formatting style.
    If `sort_by_name` is set to True, the
    Subreddits will be sorted by their name,
    in descending order. Otherwise, the
    program will attempt to pull data from past
    runs using `store.newest()`. If nothing
    was found, this defaults to sort_by_name's
    sorting mechanism (descending, by names)
    """
    result = []
    if sort_by_name:
        result.append('Rank | Name | Subscribers')
        sub_info = sorted(get_sub_info().items(), reverse=True, key=lambda s: s[1])
        for idx, sub in enumerate(sub_info):
            result.append(f'{idx + 1} | /r/{sub[0]} | {sub[1]:,}')

    return '  \n'.join(result)

