import datetime
from typing import Dict, Optional, NamedTuple, Tuple

import psycopg2


class CollectionMetadata(NamedTuple):
    id: int
    day: datetime.date


class SubredditEntry(NamedTuple):
    rank: int
    subreddit: str
    count: int


class CountDifference(NamedTuple):
    rank_difference: int
    count_difference: int


SubredditCounts = Tuple[SubredditEntry, ...]
SubredditCountDifferences = Dict[str, Optional[CountDifference]]


def load_subreddits(postgresql: psycopg2.extensions.connection) -> Tuple[str, ...]:
    """Load configured subreddit names."""

    cursor = postgresql.cursor()
    cursor.execute('SELECT name FROM subreddit WHERE enabled = true')
    return tuple(name for (name,) in cursor)


def previous_collection(
    postgresql: psycopg2.extensions.connection,
    collection: CollectionMetadata,
) -> Optional[CollectionMetadata]:
    """Fetch the last collection before the given collection."""

    cursor = postgresql.cursor()
    cursor.execute(
        'SELECT id, day FROM collection WHERE id < %s ORDER BY id DESC LIMIT 1',
        (collection.id,),
    )
    row = cursor.fetchone()
    if row:
        return CollectionMetadata(id=row[0], day=row[1])
    return None


def todays_collection(postgresql: psycopg2.extensions.connection) -> Optional[CollectionMetadata]:
    """Fetch today's collection, if present."""

    cursor = postgresql.cursor()
    cursor.execute('SELECT id, day FROM collection WHERE day = current_date')
    row = cursor.fetchone()
    if row:
        return CollectionMetadata(id=row[0], day=row[1])
    return None


def store_collection(
    postgresql: psycopg2.extensions.connection,
    counts: Dict[str, int],
    current_collection: Optional[CollectionMetadata],
) -> int:
    """Store counts to the current or given collection and return its ID."""

    cursor = postgresql.cursor()
    with postgresql:  # transaction
        if current_collection is None:
            cursor.execute('INSERT INTO collection (day) VALUES (current_date) RETURNING id')
            (collection_id,) = cursor.fetchone()
        else:
            collection_id = current_collection.id

        for name, count in counts.items():
            cursor.execute(
                'INSERT INTO subscriber_count (collection_id, subreddit, count) VALUES (%s, %s, %s)',
                (collection_id, name, count),
            )

    return collection_id


def ordered_subreddit_counts(
    postgresql: psycopg2.extensions.connection,
    collection: CollectionMetadata,
) -> SubredditCounts:
    """Return subreddit counts for the given collection, ordered by count."""

    cursor = postgresql.cursor()
    cursor.execute(
        'SELECT subreddit, count FROM subscriber_count WHERE collection_id = %s ORDER BY count DESC',
        (collection.id,),
    )

    return tuple(
        SubredditEntry(rank=rank, subreddit=row[0], count=row[1])
        for rank, row in enumerate(cursor, start=1)
    )


def differences(last: SubredditCounts, now: SubredditCounts) -> SubredditCountDifferences:
    """Compute the difference in ranks and counts from `last` to `now`.

    If the subreddit is not found in `last`, `None` will be set instead of the count and rank.
    """

    differences = {}
    for entry in now:
        subreddit = entry.subreddit

        # This has pretty awful performance. But for something that runs once a month,
        # that's fine, let's not waste my time optimizing this. If we wanted this to
        # be super fast, we would write some single PostgreSQL super-query with window
        # functions and "RANK()" to have the database do all of this for us.
        last_entry: Optional[SubredditEntry] = next(
            (record for record in last if record.subreddit == subreddit),
            None
        )

        if last_entry:
            differences[subreddit] = CountDifference(
                rank_difference=-(entry.rank - last_entry.rank),
                count_difference=entry.count - last_entry.count,
            )

        else:
            differences[subreddit] = None

    return differences

def discord_links(postgresql: psycopg2.extensions.connection) -> Dict[str, str]:
    """Return Discord invite links from the database."""

    cursor = postgresql.cursor()
    cursor.execute('SELECT name, invite_code FROM subreddit WHERE invite_code IS NOT NULL')
    return {
        name: f'https://discord.gg/{code}'
        for name, code in cursor
    }
