"""Creates various parsers and subparsers for the CLI."""

import argparse
import sys
import json


def handle_extract(args: argparse.Namespace):
    """
    Handles input given to the `extractor` Command.
    """


    if args.include_r:
        result = [
            ''.join(
                c for c in l if c.isalpha()
            ) for l in args.infile if 'Rank' not in l
        ]
    else:
        result = [
            ''.join(
                c for c in l if c.isalpha()
            ).lstrip('/r/') for l in args.infile if 'Rank' not in l
        ]
    print(result)
    args.outfile.write(json.dumps(sorted(result), indent=args.indent))
    args.outfile.write('\n')
    args.outfile.close()


def add_extractor(subparsers: argparse.ArgumentParser):
    """
    Adds the Extractor parser to the given subparsers.
    This parser is used to determine the outfile, infile,
    as well as other options for configuring the output
    of the extract command, for example the indentation.
    """

    extractor = subparsers.add_parser(
        'extract',
        help='Extract the Subreddit Names from the specified file.'
    )
    extractor.add_argument(
        'infile',
        help='The file to read data from',
        type=argparse.FileType()
    )
    extractor.add_argument(
        '-o', '--outfile',
        help='The file to write results to.',
        type=argparse.FileType(mode='r'),
        default=sys.stdout
    )
    extractor.add_argument(
        '-i', '--indent',
        help=('The amount of spaces to use for '
              'indenting the Array. Defaults to 4.');
        type=int,
        default=4,
    )
    extractor.add_argument(
        '-r', '--include-r',
        help=('Whether to include the /r/ prepending '
              'the Subreddit names or not. Defaults to '
              'not including them.'),
        type=bool,
        default=False
    )
    extractor.set_defaults(func=handle_extract)


