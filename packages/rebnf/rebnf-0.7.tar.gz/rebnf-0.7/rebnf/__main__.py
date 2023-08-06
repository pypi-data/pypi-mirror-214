"""
ReBNF: Regexes for Extended Backus-Naur Form (EBNF)

Copyright (C) 2023 opsocket <opsocket@pm.me>

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <https://www.gnu.org/licenses>.
"""
from . import tokenize, parse, __ascii__, __version__
import argparse

__description__ = Rf"""

{__ascii__} v{__version__}

"""


def tabulate(data, headers=None):
    """
    Utility to generate the tokens table string
    """
    table_data = [headers] + data if headers else data
    # determine the maximum width of each column
    col_widths = [
        max(len(str(row[i])) for row in table_data) for i in range(len(table_data[0]))
    ]
    formatted_rows = []
    for row in table_data:
        formatted_row = [str(row[i]).ljust(col_widths[i]) for i in range(len(row))]
        formatted_rows.append(formatted_row)
    return "\n".join(" ".join(row) for row in formatted_rows)


def fmtok(tok):
    """
    Utility to print comprehensive token values
    """
    for c in "\n\t\r\f\b":
        if tok.value.count(c):
            return repr(tok.value)
    if tok.value.startswith("'"):
        return f'"{tok.value}"'
    else:
        return f"'{tok.value}'"


def main():
    parser = argparse.ArgumentParser(
        "rebnf",
        description=__description__,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    base_parser = argparse.ArgumentParser(add_help=False)
    base_parser.add_argument("filepath", type=str, help="path to the file to parse")

    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    # create the subparser for 'tokenize'
    tokenize_parser = subparsers.add_parser("tokenize", parents=[base_parser])
    tokenize_parser.add_argument(
        "-t", "--table", action="store_true", help="prints tokens as a table"
    )
    tokenize_parser.set_defaults(func=tokenize)

    # create the subparser for 'parse'
    parse_parser = subparsers.add_parser("parse", parents=[base_parser])
    parse_parser.add_argument(
        "-p", "--pretty", action="store_true", help="prints a pretty output"
    )
    parse_parser.set_defaults(func=parse)

    # parse command-line arguments
    args = parser.parse_args()

    # call appropriate function based on subcommand
    if hasattr(args, "func"):
        with open(args.filepath, "r") as code:
            if args.subcommand == "tokenize":
                tokens = args.func(code.read())
                print(
                    tabulate(
                        [[t.lineno, t.column, t.lexpos, t.type, fmtok(t)] for t in tokens],
                        headers=[
                            "LINE",
                            "COL",
                            "POS",
                            "TYPE",
                            "TOKEN",
                        ],
                    )
                )
            else:
                if args.pretty:
                    from pprint import pprint
                    pprint(args.func(code.read()))
                else:
                    print(args.func(code.read()))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
