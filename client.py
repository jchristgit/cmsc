"""Handles interacting with Reddit's API using PRAW."""

import json
import praw

with open('config.json', 'r') as config:
    config = json.load(config)
    reddit = praw.Reddit(
        client_id=config['reddit']['client_id'],
        client_secret=config['reddit']['client_secret'],
        user_agent=config['reddit']['user_agent']
    )


def get_sub_count(subreddit_name: str) -> int:
    """
    Retrieves the Subreddit count for the specified Subreddit.
    """

    return reddit.subreddit(subreddit_name).subscribers
