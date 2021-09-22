"""Leanpub Actions for GitHub Actions Workflows."""

import datetime
import sys

import click

from leanpub_multi_action.leanpub import Leanpub


@click.command()
@click.option(
    "--leanpub_api_key",
    envvar="LEANPUB_API_KEY",
    help="Leanpub API Key. Will also look for 'LEANPUB_API_KEY' environment variable.",
)
@click.option(
    "--book_slug",
    envvar="LEANPUB_BOOK_SLUG",
    help=(
        "Book Slug is the unique book name on Leanpub.com (i.e. the 'mybook' portion of https://leanpub.com/mybook)."
        "Will also look for 'LEANPUB_BOOK_SLUG' environment variable."
    ),
)
@click.option("--preview", is_flag=True, help="Preview a book on Leanpub.")
@click.option("--publish", is_flag=True, help="Publish a book on Leanpub.")
@click.option("--check_status", is_flag=True, help="Check the job status of a Preview or Publish on Leanpub.")
def main(
    leanpub_api_key: str = None,
    book_slug: str = None,
    preview: bool = False,
    publish: bool = False,
    check_status: bool = False,
) -> int:
    """Entrypoint into our script.

    Publish, Preview, or Check Status on an existing Publish/Preview job.

    Args:
        leanpub_api_key (bool): API Key for the Leanpub API.
            If not set, will error out.
        book_slug (bool): Unique book name from the leanpub URL of the book.
            i.e. the 'mybook' portion of https://leanpub.com/mybook
            If not set, will error out.
        check_status(bool): Check the job status of a Preview or Publish on Leanpub.

    Returns:
        int: exit_code as an integer to return to OS
    """
    exit_code = 0

    # Attempt to find API Key
    if not leanpub_api_key:
        exit_code = 1
        print("No Leanpub API Key Found!")
        return exit_code

    # Attempt to find Book Slug
    if not book_slug:
        exit_code = 1
        print("No Leanpub Book Slug Found!")
        return exit_code

    print("Leanpub API Key and Book Slug found")

    # We need to be doing one of the three possible actions
    if not publish and not preview and not check_status:
        exit_code = 1
        print("Must either Publish, Preview, or Check Status!")
        return exit_code

    err = None

    # Instantiate the Leanpub client
    leanpub = Leanpub(leanpub_api_key=leanpub_api_key)

    # Check if we are previewing
    if preview:
        print(f"Generating a Preview of '{book_slug}'")
        resp, err = leanpub.preview(book_slug=book_slug)
        if err is not None:
            print(err)
            exit_code = 1
        elif resp.status_code == 200:
            print(f"Preview job started at {datetime.datetime.utcnow()}")
        else:
            print("Unknown error has occurred!")
            exit_code = 1

    # Check if we are publishing
    if publish:
        pass  # TODO: build this

    # Check if we are checking :lulz:
    if check_status:
        pass  # TODO: make this happen

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
