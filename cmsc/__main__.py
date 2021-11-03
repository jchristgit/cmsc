"""Champion Mains Subscriber Counter.

Fetches subreddit counts for a configured list of subreddits into the
PostgreSQL database and posts a summary of subscriber counts to reddit.  The
actions to take are controlled via the CLI flags in the "actions" group.
"""

import argparse
import logging
import os
import sys

import praw
import psycopg2

from . import client
from . import persistence


logging.basicConfig(
    format="%(name)s | %(levelname)s | %(message)s"
)
log = logging.getLogger('cmsc')


def get_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='cmsc',
        description=description,
    )
    parser.add_argument(
        '-l',
        '--log-level',
        help="At which level to produce logging output. Defaults to INFO.",
        default='INFO',
        choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
    )
    parser.add_argument(
        '--log-format',
        help=(
            "Logging format to use. By default, no timestamps are included "
            "in the logs, under the assumption that we are logging to "
            "or a similar log ingester which adds its own timestamps. This "
            "option can be used to add a timestamp to the log format."
        ),
    )

    actions = parser.add_argument_group(
        title='actions',
        description="Controls the behaviour of this run.",
    )
    actions.add_argument(
        '--no-update',
        action='store_false',
        help=(
            "Skip the default behaviour of loading subscriber counts "
            "from reddit and storing them into PostgreSQL."
        ),
        default=True,
        dest='update',
    )
    actions.add_argument(
        '--post-to',
        help=(
            "Post subscriber counts and differences with the previous month "
            "to the given subreddit."
        ),
    )

    connections = parser.add_argument_group(
        title='connections',
        description=(
            "Connection credentials for backing and upstream services. "
            "All options listed here are mandatory."
        ),
    )
    connections.add_argument(
        '--dsn',
        help=(
            "PostgreSQL DSN to use for connecting to the database. Can be "
            "anything that libpq accepts. [$POSTGRES_DSN]"
        ),
        default=os.getenv('POSTGRES_DSN'),
    )
    connections.add_argument(
        '--reddit-username',
        help="Reddit username for the posting bot. [$REDDIT_USERNAME]",
        default=os.getenv('REDDIT_USERNAME'),
    )
    connections.add_argument(
        '--reddit-password',
        help="Reddit password for the posting bot. [$REDDIT_PASSWORD]",
        default=os.getenv('REDDIT_PASSWORD'),
    )
    connections.add_argument(
        '--reddit-client-id',
        help="Reddit OAuth Client ID for the posting bot. [$REDDIT_CLIENT_ID]",
        default=os.getenv('REDDIT_CLIENT_ID'),
    )
    connections.add_argument(
        '--reddit-client-secret',
        help="Reddit OAuth Client Secret for the posting bot. [$REDDIT_CLIENT_SECRET]",
        default=os.getenv('REDDIT_CLIENT_SECRET'),
    )
    connections.add_argument(
        '--reddit-user-agent',
        help=(
            "The user agent to use for connecting to reddit to. Please see "
            "https://github.com/reddit-archive/reddit/wiki/API for Reddit's "
            "guidelines on choosing a user agent. [$REDDIT_USER_AGENT]"
        ),
        default=os.getenv('REDDIT_USER_AGENT'),
    )

    output = parser.add_argument_group('output', "Options influencing the bot output to Reddit.")
    output.add_argument(
        '--contact',
        help=(
            "Who to contact for any issues with the bot's post. Added to the "
            "table that is posted to reddit. For example: `--contact "
            "'joe#0001 on Discord'` will mention the contact method in the "
            "resulting output to allow users to have a place to report issues "
            "to. Not passing this flag will not add any hint as to whom to "
            "contact. [$CONTACT]"
        ),
        default=os.getenv('CONTACT'),
    )
    return parser


def main() -> int:
    args = get_parser(__doc__).parse_args()
    log_level = getattr(logging, args.log_level)
    log.setLevel(log_level)
    if args.log_format:
        root_logger = logging.getLogger('')
        formatter = logging.Formatter(args.log_format)
        root_logger.handlers[0].setFormatter(formatter)

    reddit = praw.Reddit(
        username=args.reddit_username,
        password=args.reddit_password,
        client_id=args.reddit_client_id,
        client_secret=args.reddit_client_secret,
        user_agent=args.reddit_user_agent,
    )
    postgresql = psycopg2.connect(args.dsn)

    if args.update:  # Defaults to on
        subreddits = persistence.load_subreddits(postgresql)
        log.info("Got %d subreddits from database.", len(subreddits))
        counts = client.load_subscriber_counts(reddit, subreddits)
        log.info("Fetched %d subscriber counts.", len(counts))
        todays_collection = persistence.todays_collection(postgresql)
        if todays_collection:
            # This would crash in the database due to primary key violation
            log.critical("Refusing to overwrite existing collection for today (%d).", todays_collection.id)
            return 1

        collection = persistence.store_collection(postgresql, counts, todays_collection)
        log.info("Stored subscriber counts to collection %d.", collection)

    if args.post_to is not None:
        current_collection = persistence.todays_collection(postgresql)
        if current_collection is None:
            log.critical("No collection for today present to post data from.")
            return 1

        previous_collection = persistence.previous_collection(postgresql, current_collection)
        if previous_collection is None:
            log.critical("No previous collection present to compare data to.")
            return 1

        if current_collection.day == previous_collection.day:
            log.critical("Both collections made on the same day.")
            return 1

        log.info(
            "Comparing collection from %s to %s.",
            current_collection.day.strftime('%Y-%m-%d'),
            previous_collection.day.strftime('%Y-%m-%d'),
        )

        current_counts = persistence.ordered_subreddit_counts(postgresql, current_collection)
        previous_counts = persistence.ordered_subreddit_counts(postgresql, previous_collection)
        differences = persistence.differences(previous_counts, current_counts)
        links = persistence.discord_links(postgresql)
        client.post_results(
            reddit=reddit,
            subreddit_name=args.post_to,
            counts=current_counts,
            links=links,
            differences=differences,
            contact=args.contact,
            last_update=previous_collection.day,
        )
        log.info("Results posted to /r/%s.", args.post_to)

    return 0


if __name__ == '__main__':
    sys.exit(main())
