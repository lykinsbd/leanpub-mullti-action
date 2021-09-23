"""Tasks for use with Invoke."""
import os
import sys

from invoke import task

try:
    import toml
except ImportError:
    sys.exit("Please make sure to `pip install toml` or enable the Poetry shell and run `poetry install`.")


PYPROJECT_CONFIG = toml.load("pyproject.toml")
TOOL_CONFIG = PYPROJECT_CONFIG["tool"]["poetry"]

# Can be set to a separate Python version to be used for launching or building image
INVOKE_PYTHON_VER = os.getenv("INVOKE_PYTHON_VER", "3.9")
# Name of the docker image/image
IMAGE_NAME = os.getenv("IMAGE_NAME", TOOL_CONFIG["name"])
# Tag for the image
IMAGE_VER = os.getenv("IMAGE_VER", f"{TOOL_CONFIG['version']}")
# Leanpub API Key for testing
LEANPUB_API_KEY = os.getenv("LEANPUB_API_KEY", "test_api_key!")
# Leanpub Book Slug for testing
LEANPUB_BOOK_SLUG = os.getenv("LEANPUB_BOOK_SLUG", "test_book_slug")

# Gather current working directory for Docker commands
PWD = os.getcwd()


def run_cmd(context, exec_cmd):
    """Wrapper to run the invoke task commands.

    Args:
        context ([invoke.task]): Invoke task object.
        exec_cmd ([str]): Command to run.

    Returns:
        result (obj): Contains Invoke result from running task.
    """
    print(f"LOCAL - Running command {exec_cmd}")
    result = context.run(exec_cmd, pty=True)

    return result


@task(
    help={
        "cache": "Whether to use Docker's cache when building images (default enabled)",
        "force_rm": "Always remove intermediate images",
        "hide": "Suppress output from Docker",
    }
)
def build(context, cache=True, force_rm=False, hide=False):
    """Build the Python package and Docker image."""
    python_name = f"{IMAGE_NAME}-{IMAGE_VER}"
    docker_name = f"{IMAGE_NAME}:{IMAGE_VER}"

    print(f"Building Python package {python_name}")
    py_command = "poetry build"
    print(py_command)
    result = context.run(py_command, pty=True)
    if result.exited != 0:
        print(f"Failed to build Python package {python_name}\nError: {result.stderr}")
        return

    print(f"Building Docker image {docker_name}")
    command = (
        f"docker build --tag {docker_name} "
        f"--build-arg LMA_VERSION={IMAGE_VER} --build-arg WHEEL_DIR=dist "
        f"-f Dockerfile ."
    )

    if not cache:
        command += " --no-cache"
    if force_rm:
        command += " --force-rm"

    print(f"{command}")
    result = context.run(command, hide=hide)
    if result.exited != 0:
        print(f"Failed to build Docker image {docker_name}\nError: {result.stderr}")


@task
def clean(context):
    """Remove the project specific image."""
    print(f"Attempting to forcefully remove image {IMAGE_NAME}:{IMAGE_VER}")
    context.run(f"docker rmi {IMAGE_NAME}:{IMAGE_VER} --force")
    print(f"Successfully removed image {IMAGE_NAME}:{IMAGE_VER}")


@task
def rebuild(context):
    """Clean the Docker image and then rebuild without using cache."""
    clean(context)
    build(context, cache=False)


@task
def pytest(context):
    """Run pytest test cases."""
    exec_cmd = "pytest"
    run_cmd(context, exec_cmd)


@task
def black(context):
    """Run black to check that Python files adherence to black standards."""
    exec_cmd = "black --check --diff ."
    run_cmd(context, exec_cmd)


@task
def flake8(context):
    """Run flake8 code analysis."""
    exec_cmd = "flake8 ."
    run_cmd(context, exec_cmd)


@task
def pylint(context):
    """Run pylint code analysis."""
    exec_cmd = 'find . -name "*.py" | xargs pylint'
    run_cmd(context, exec_cmd)


@task
def yamllint(context):
    """Run yamllint to validate formatting adheres to NTC defined YAML standards."""
    exec_cmd = "yamllint ."
    run_cmd(context, exec_cmd)


@task
def pydocstyle(context):
    """Run pydocstyle to validate docstring formatting adheres to NTC defined standards."""
    exec_cmd = "pydocstyle ."
    run_cmd(context, exec_cmd)


@task
def bandit(context):
    """Run bandit to validate basic static code security analysis."""
    exec_cmd = "bandit --recursive ./ --configfile .bandit.yml"
    run_cmd(context, exec_cmd)


@task
def cli(context):
    """Enter the image to perform troubleshooting or dev work."""
    dev = f"docker run -it -v {PWD}:/local {IMAGE_NAME}:{IMAGE_VER} /bin/bash"
    print(f"{dev}")
    context.run(f"{dev}", pty=True)


@task
def preview(context):
    """Test the 'Preview' functionality in the container."""
    command = (
        f"docker run -t "
        f"-e LEANPUB_API_KEY={LEANPUB_API_KEY} -e LEANPUB_BOOK_SLUG={LEANPUB_BOOK_SLUG} "
        f"{IMAGE_NAME}:{IMAGE_VER} --preview"
    )
    # print(f"{command}")  # Commenting out as this can print secrets
    context.run(f"{command}", pty=True)


@task
def tests(context):
    """Run all tests for this repository."""
    black(context)
    flake8(context)
    pylint(context)
    yamllint(context)
    pydocstyle(context)
    bandit(context)
    pytest(context)

    print("All tests have passed!")


@task
def release(context):
    """Start a Release on GitHub."""
    print(f"Starting a release of v{IMAGE_VER} on GitHub!")
    checkout = "git checkout main"
    print(checkout)
    result = context.run(checkout, pty=True)
    if result.exited != 0:
        print(f"Failed to checkout main!\nError: {result.stderr}")
        return

    pull = "git pull origin main"
    print(pull)
    result = context.run(pull, pty=True)
    if result.exited != 0:
        print(f"Failed to pull from origin main!\nError: {result.stderr}")
        return

    tag = f"git tag v{IMAGE_VER}"
    print(tag)
    result = context.run(tag, pty=True)
    if result.exited != 0:
        print(f"Failed to create the tag 'v{IMAGE_VER}'!\nError: {result.stderr}")
        return

    tag_push = "git push --tags"
    print(tag_push)
    result = context.run(tag_push, pty=True)
    if result.exited != 0:
        print(f"Failed to push the tag 'v{IMAGE_VER}'!\nError: {result.stderr}")
        return
