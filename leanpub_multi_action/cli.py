"""Leanpub Actions for GitHub Actions Workflows."""

import os
import sys

import click


@click.command()
@click.option("--leanpub_api_key", help="Leanpub API Key")
def main(leanpub_api_key: str = None) -> int:
    """Entrypoint into our script.

    Args:
        leanpub_api_key (str): API Key for the Leanpub API.
            If not provided, will attempt to gather from the
            LEANPUB_API_KEY Environment Variable.
            If neither are set, will error out.

    Returns:
        int: exit_code as an integer to return to OS
    """
    exit_code = 0

    # Attempt to find API Key
    leanpub_api_key = leanpub_api_key or os.environ.get("LEANPUB_API_KEY", False)
    if not leanpub_api_key:
        exit_code = 1
        print("No Leanpub API Key Found!")
        return exit_code

    err = None

    if err is not None:
        print(err)
        exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
