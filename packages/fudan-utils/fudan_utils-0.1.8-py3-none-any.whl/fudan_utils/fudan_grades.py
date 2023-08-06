#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2023-06-15
Purpose: Get Fudan grades from jwfw
"""

import argparse
from pathlib import Path
from fudan_utils.fudan import get_account, FudanJwfw
from fudan_utils.config import fudan_uis_duplicated_login_marker
from fudan_utils.utils import create_html_table


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Get Fudan grades from jwfw',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        '-j', '--json', help='output in json format', action='store_true'
    )

    parser.add_argument(
        '-t', '--html-table', help='output in html table format', action='store_true'
    )

    return parser.parse_args()


def main():
    """Make a jazz noise here"""

    args = get_args()
    jwfw = FudanJwfw(*get_account(verbose=False), verbose=False)
    try:
        jwfw.login()
        if fudan_uis_duplicated_login_marker in (grades_html := jwfw.get_grades_html()):
            grades_html = jwfw.get_grades_html()
        grades = jwfw.parse_grades_html(grades_html)
    except Exception as e:
        raise e
    finally:
        jwfw.close(exit=False)

    if args.json:
        import json

        print(json.dumps(grades, ensure_ascii=False, indent=2))
        return

    if args.html_table:
        print(create_html_table(grades))
        return

    from tabulate import tabulate

    print(tabulate(grades, headers='keys'))


if __name__ == '__main__':
    main()
