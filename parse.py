"""Creates various parsers and subparsers for the CLI."""

import argparse
import sys
import json

import table_builder


def handle_extract(args: argparse.Namespace):
    """
    Handles input given to the `extractor` Command.
    """

    if args.include_r > 0:
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

    args.outfile.write(
        json.dumps(
            sorted(
                result,
                key=lambda s: s[0].lower() if s else s
            ),
            indent=args.indent
        )
    )

    if args.outfile is sys.stdout:
        args.outfile.write('\n')
    else:
        print(f'Wrote extracted Subreddit Names to {args.outfile.name}.')
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
        type=argparse.FileType(mode='w+'),
        default=sys.stdout
    )
    extractor.add_argument(
        '-i', '--indent',
        help=('The amount of spaces to use for '
              'indenting the Array. Defaults to 4.'),
        type=int,
        default=4,
    )
    extractor.add_argument(
        '-r', '--include-r',
        help=('Whether to include the /r/ prepending '
              'the Subreddit names. Defaults to '
              'not including them.'),
        action='count',
        default=0
    )
    extractor.set_defaults(func=handle_extract)


def handle_build(args: argparse.Namespace):
    """
    Handles the invocation of the `build` Command.
    Provides verbosity options.
    """

    table = table_builder.get_table(args.nocomp > 0)

    args.outfile.write(table)
    if args.outfile is sys.stdout:
        args.outfile.write('\n')
    else:
        print('Wrote results to specified file.')
    args.outfile.close()


def add_builder(subparsers: argparse.ArgumentParser):
    """
    Adds the `build` Command to the parser,
    which is used to build the Reddit tables.
    """

    builder = subparsers.add_parser(
        'build',
        help='Builds tables to be used in Reddit.'
    )

    builder.add_argument(
        '-o', '--outfile',
        help=('The file to which the table should '
              'be written. Defaults to printing to '
              'console.'),
        type=argparse.FileType(mode='w+'),
        default=sys.stdout
    )

    builder.add_argument(
        '-nc', '--nocomp',
        help=('If this flag is given, then the '
              'application will not attempt to compare '
              'the results of the subscriber counting '
              'to the results of previous months (and '
              'thus, not display any differences '
              'between them in the output'),
        action='count',
        default=0
    )
    
    builder.set_defaults(func=handle_build)

