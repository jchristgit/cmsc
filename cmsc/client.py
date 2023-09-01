"""Reddit client."""

import datetime
import logging
from typing import Dict, Tuple, Optional, List

import praw
import prawcore.exceptions

from .persistence import SubredditCounts, SubredditCountDifferences


log = logging.getLogger(__name__)


def load_subscriber_counts(
    reddit: praw.Reddit,
    subreddits: Tuple[str, ...],
) -> Dict[str, int]:
    counts = {}
    for name in subreddits:
        subreddit = reddit.subreddit(name)
        try:
            counts[subreddit.display_name] = subreddit.subscribers
        except prawcore.exceptions.NotFound:
            log.warning("Not fetching subscribers for subreddit %r (not found)", name)
        except prawcore.exceptions.Forbidden:
            log.warning("Not fetching subscribers for subreddit %r (forbidden)", name)
    return counts


def post_results(
    reddit: praw.Reddit,
    subreddit_name: str,
    counts: SubredditCounts,
    links: Dict[str, Optional[str]],
    differences: SubredditCountDifferences,
    contact: str,
    last_update: datetime.date,
) -> None:
    """Post results of the collection to the given subreddit."""

    content: List[str] = [
        f"Hey, I'm a bot! Should there be any problem with this, contact {contact}.",
        '',
        'Rank | Name | Subscribers | Subscriber difference | Rank difference | Discord invite',
        '---|---|---|---|---|--',
    ]

    for entry in counts:
        difference = differences.get(entry.subreddit)
        discord_invite = links.get(entry.subreddit, '')
        if difference:
            content.append(
                f'{entry.rank} | r/{entry.subreddit} | {entry.count:,} | {difference.count_difference:+} | {difference.rank_difference:+} | {discord_invite}'
            )
        else:
            content.append(
                f'{entry.rank} | r/{entry.subreddit} | {entry.count:,} | | | {discord_invite}'
            )

    # Add some newlines (joined on '\n').
    content.append('')
    content.append('')

    content.append(f"The last count was retrieved on {last_update.strftime('%Y-%m-%d')}.")
    body = '\n'.join(content)
    subreddit = reddit.subreddit(subreddit_name)
    subreddit.submit("Monthly sub count statistics", selftext=body, send_replies=False)
