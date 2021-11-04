# Champion Mains Subscriber Counter

### Installation

Requires:

- Python 3.7+ with the `praw` package
- PostgreSQL with the schema in `schema.sql` (adjust user ownership as necessary)
- If posting to Reddit is desired, a Reddit user account

### Usage

```
$ python -m cmsc --help
usage: cmsc [-h] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--log-format LOG_FORMAT] [--no-update] [--post-to POST_TO] [--dsn DSN]
            [--reddit-username REDDIT_USERNAME] [--reddit-password REDDIT_PASSWORD] [--reddit-client-id REDDIT_CLIENT_ID]
            [--reddit-client-secret REDDIT_CLIENT_SECRET] [--reddit-user-agent REDDIT_USER_AGENT] [--contact CONTACT]

Champion Mains Subscriber Counter. Fetches subreddit counts for a configured list of subreddits into the PostgreSQL database and posts
a summary of subscriber counts to reddit. The actions to take are controlled via the CLI flags in the "actions" group.

optional arguments:
  -h, --help            show this help message and exit
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        At which level to produce logging output. Defaults to INFO.
  --log-format LOG_FORMAT
                        Logging format to use. By default, no timestamps are included in the logs, under the assumption that we are
                        logging to or a similar log ingester which adds its own timestamps. This option can be used to add a timestamp
                        to the log format.

actions:
  Controls the behaviour of this run.

  --no-update           Skip the default behaviour of loading subscriber counts from reddit and storing them into PostgreSQL.
  --post-to POST_TO     Post subscriber counts and differences with the previous month to the given subreddit.

connections:
  Connection credentials for backing and upstream services. All options listed here are mandatory.

  --dsn DSN             PostgreSQL DSN to use for connecting to the database. Can be anything that libpq accepts. [$POSTGRES_DSN]
  --reddit-username REDDIT_USERNAME
                        Reddit username for the posting bot. [$REDDIT_USERNAME]
  --reddit-password REDDIT_PASSWORD
                        Reddit password for the posting bot. [$REDDIT_PASSWORD]
  --reddit-client-id REDDIT_CLIENT_ID
                        Reddit OAuth Client ID for the posting bot. [$REDDIT_CLIENT_ID]
  --reddit-client-secret REDDIT_CLIENT_SECRET
                        Reddit OAuth Client Secret for the posting bot. [$REDDIT_CLIENT_SECRET]
  --reddit-user-agent REDDIT_USER_AGENT
                        The user agent to use for connecting to reddit to. Please see https://github.com/reddit-
                        archive/reddit/wiki/API for Reddit's guidelines on choosing a user agent. [$REDDIT_USER_AGENT]

output:
  Options influencing the bot output to Reddit.

  --contact CONTACT     Who to contact for any issues with the bot's post. Added to the table that is posted to reddit. For example:
                        `--contact 'joe#0001 on Discord'` will mention the contact method in the resulting output to allow users to
                        have a place to report issues to. Not passing this flag will not add any hint as to whom to contact.
                        [$CONTACT]
```

### Naming

This project was born for the subreddit subscriber counting done for the
"Champion Mains" community on Reddit, but can be used anywhere.
