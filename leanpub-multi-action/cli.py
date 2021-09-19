"""Leanpub Actions for GitHub Actions Workflows"""
import sys

import click


@click.command()
@click.option("--test", help="Test argument")
def main(test: str) -> int:
    """Entrypoint into our script.

    Args:
        test (str): testing and stuff

    Returns:
        int: exit_code as an integer to return to OS
    """
    exit_code = 0
    print(test)
    return exit_code


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
