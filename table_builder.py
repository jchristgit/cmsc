"""Builds tables for use in Reddit."""

import json

import client
import store


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
    Additionally, this function stores the
    newly created list using the `store`
    module.
    """

    with open('config/config.json') as config:
        subreddits = json.load(config)['subreddits']
    result = {}
    for sub in subreddits:
        sub_info = client.get_sub(sub)
        result[sub_info.display_name] = sub_info.subscribers
    store.store(result)

    return result


def get_table(no_comp=False) -> str:
    """
    Returns a string containing a table in
    Reddit's formatting style.
    This Function will attempt to pull data from past
    runs using `store.newest()`. If nothing
    was found, this defaults to sort_by_name's
    sorting mechanism (descending, by names)
    If `no_comp` is passed as `True`, then this
    function will never attempt to compare to
    any data found from `store`.
    """

    result = []
    newest = store.newest()
    print('Getting Subreddit information, this may take a moment... ', end='', flush=True)
    sub_info = sorted(get_sub_info().items(), reverse=True, key=lambda s: s[1])
    print('done.')

    if no_comp or newest is None:
        if no_comp:
            print('Disabled comparison of results for this run.')
        else:
            print('Found no data from previous runs.')

        result.append('Rank | Name | Subscribers')
        result.append('---|---|---')
        for idx, sub in enumerate(sub_info):
            result.append(
                f'{idx + 1} | /r/{sub[0]} | {sub[1]:,}'
            )

    else:
        print(f'Found existing file from {newest[0]}, comparing to it\n')
        with open('config/config.json') as config:
            subreddits = json.load(config)['subreddits']

        last_month_sorted = sorted(
            (
                (sub_name, subscribers)
                for sub_name, subscribers
                in newest[1].items()
            ),
            key=lambda sub_tuple: sub_tuple[1],
            reverse=True
        )

        result.append('Rank | Name | Subscribers | Subscriber difference | Rank difference | Discord invite')
        result.append('---|---|---|---|---|--')
        for idx, sub in enumerate(sub_info):
            sub_difference = sub[1] - newest[1].get(sub[0], 0)

            rank_last_month = 0
            for name, _ in last_month_sorted:
                rank_last_month += 1
                if name == sub[0]:
                    break

            rank_difference = -(idx + 1 - rank_last_month)
            links = ' '.join(f'https://{link}' for link in subreddits[sub[0]].split())
            result.append(
                f'{idx + 1} | /r/{sub[0]} | {sub[1]:,} | {sub_difference:+} | {rank_difference:+} | {links}'
            )

    return '  \n'.join(result)
