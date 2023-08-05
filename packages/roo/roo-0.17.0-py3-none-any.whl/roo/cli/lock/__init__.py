import logging
import os
import pathlib

import click
from roo.console import console
from roo.locker import Locker
from roo.parsers.exceptions import ParsingError
from roo.parsers.lock import Lock
from roo.parsers.rproject import RProject
from roo.resolver import CannotResolveError


logger = logging.getLogger(__file__)


@click.command(help="Creates a lock file from the rproject.toml")
@click.option(
    "--quiet", is_flag=True, default=False,
    help="Produce no output")
@click.option(
    "--overwrite", is_flag=True, default=False,
    help="Force recreation of the roo.lock overwriting the current one")
@click.option(
    "--conservative", is_flag=True, default=False,
    help="Ensures that only minimal changes will be performed to the lock."
)
@click.option(
    "--fix-changed-hash", is_flag=True, default=False,
    help=(
        "Only fix change of recorded package hash. "
        "NOTE: this might hide a security threat."
    )
)
def lock(quiet, overwrite, conservative, fix_changed_hash):
    ensure_lock(overwrite, conservative, fix_changed_hash)


def ensure_lock(
        overwrite: bool, conservative: bool, fix_changed_hash: bool
) -> Lock:
    """
    Ensure that a lock file is present and sync.

    If the conservative flag is None, it means that whatever is in the
    old lock should be honored. If there's no old lock, it's equivalent to
    False. This is to prevent re-locking during install.
    """
    try:
        rproject = RProject.parse(pathlib.Path(".") / "rproject.toml")
    except IOError:
        raise click.ClickException(
            "Unable to open rproject.toml in current directory"
        )
    lock_path = pathlib.Path(".") / "roo.lock"

    if overwrite:
        try:
            os.remove(lock_path)
        except FileNotFoundError:
            pass

    old_lock = None
    try:
        old_lock = Lock.parse(lock_path)
    except FileNotFoundError:
        console().print("[warning]Lockfile not found.[/warning]")
    except ParsingError as e:
        logger.exception("Unable to parse current lockfile")
        console().print(
            f"[error]Existing Lockfile could not be parsed: {e}.[/error]")
        raise click.ClickException(f"Unable to parse current lock file: {e}")

    if old_lock is None:
        old_lock = Lock()

    if not conservative:
        conservative = old_lock.metadata.conservative

    locker = Locker()
    try:
        if fix_changed_hash:
            new_lock = locker.fix_hash(old_lock)
        else:
            new_lock = locker.lock(
                rproject, old_lock, conservative
            )
    except CannotResolveError as e:
        raise click.ClickException(f"Unable to create lock file: {e}")

    new_lock.save(old_lock.path)
    return new_lock
