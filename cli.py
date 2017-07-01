"""Handles interacting with the User over a CLI."""

import argparse
import cmd
import json

import builder
import parse


class CMSCShell(cmd.Cmd):
    intro = 'Champion Mains Subscriber Counter'
    prompt = 'cmsc} '


    def do_table(self, _):
        """
        Builds a table from the Subreddits specified in
        config.json. Returns it in Reddit's formatting
        style for easy copy / paste.
        """

        print(builder.get_table())

    def do_extract(self, _):
        """
        A tool to extract the Subreddit Names from a
        "reddit table" posted in a file called curr_list.txt.
        """

        with open('curr_list.txt') as old_list:
            result = [
                ''.join(
                    c for c in l if c.isalpha()
                ).lstrip('/r/') for l in old_list if 'Rank' not in l
            ]
        print(len(result))
        print(json.dumps(sorted(result), indent=4))


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=('Provides utilities for generating and working with '
                     'subscriber-related data from configured Subreddits')
    )

    subparsers = parser.add_subparsers(
        title='Main Functions'
    )
    parse.add_extractor(subparsers)

    return parser.parse_args()


if __name__ == '__main__':
    print(get_args())

