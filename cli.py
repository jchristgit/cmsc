"""Handles interacting with the User over a CLI."""

import argparse

import parse


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=('Provides utilities for generating and working with '
                     'subscriber-related data from configured Subreddits')
    )

    subparsers = parser.add_subparsers(
        title='Main Functions'
    )
    parse.add_extractor(subparsers)
    parse.add_builder(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    get_args()

