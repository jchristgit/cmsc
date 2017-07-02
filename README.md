# Champion Mains Subscription Counter


### Usage
- Adjust the file `config-example.json` and rename it to `config.json`.
- Install `PRAW` using `pip3 install praw`.
- `python3 cli.py` is the main entry point for the program.

#### Commands
- `python3 cli.py --help`
Displays basic help about the program. Recommended.

- `extract`
The extract command serves as an utility for extracting the Subreddit names
out of a Reddit table that was previously generated. Several options are
configurable. Use `python3 cli.py extract --help` to read about all of them.

