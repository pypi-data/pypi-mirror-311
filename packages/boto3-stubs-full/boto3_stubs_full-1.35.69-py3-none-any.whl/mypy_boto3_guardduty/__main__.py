"""
Main CLI entrypoint.

Copyright 2024 Vlad Emelianov
"""

import sys


def print_info() -> None:
    """
    Print package info to stdout.
    """
    print(
        "Type annotations for boto3 GuardDuty 1.35.69\n"
        "Version:         1.35.69\n"
        "Builder version: 8.3.1\n"
        "Docs:            https://youtype.github.io/boto3_stubs_docs/mypy_boto3_guardduty//\n"
        "Boto3 docs:      https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/guardduty.html#guardduty\n"
        "Other services:  https://pypi.org/project/boto3-stubs/\n"
        "Changelog:       https://github.com/youtype/mypy_boto3_builder/releases"
    )


def print_version() -> None:
    """
    Print package version to stdout.
    """
    print("1.35.69")


def main() -> None:
    """
    Main CLI entrypoint.
    """
    if "--version" in sys.argv:
        return print_version()
    print_info()


if __name__ == "__main__":
    main()
