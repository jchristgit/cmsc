"""Handles interacting with Reddit's API using PRAW."""

import os
import json

import praw


config_path = os.getenv('CONFIG_FILE', 'config/config.json')

with open(config_path, 'r') as f:
    config = json.load(f)
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
