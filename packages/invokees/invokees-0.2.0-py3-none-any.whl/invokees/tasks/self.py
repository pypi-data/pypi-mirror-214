from invoke import task


@task(aliases=("init",))
def initialize(context, root=".", color=True):
    """
    Initialize configurations

    Args:
        context: invoke context.
        root: to search for python files (default: '.').
        color: whether to use colors (default: True).
    """
    # add configuration files
    # initalize pre-commit
    # add github actions
    # add github issue templates
    # add dependabot


@task
def update(context, root=".", color=True):
    """
    Update configurations

    Args:
        context: invoke context.
        root: to search for python files (default: '.').
        color: whether to use colors (default: True).
    """
    pass
    # update configuration files
    # update pre-commit
    # update github actions
    # update github issue templates
    # update dependabot
