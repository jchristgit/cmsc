"""Handles interacting with Reddit's API using PRAW."""

import json
import praw


with open('config/config.json', 'r') as config:
    config = json.load(config)
    reddit = praw.Reddit(
        username=config['reddit']['username'],
        password=config['reddit']['password'],
        client_id=config['reddit']['client_id'],
        client_secret=config['reddit']['client_secret'],
        user_agent=config['reddit']['user_agent']
    )


def get_sub(subreddit_name: str) -> praw.models.Subreddit:
    """
    Retrieves a `praw.Subreddit` object
    from the given Subreddit Name.
    """

    return reddit.subreddit(subreddit_name)
