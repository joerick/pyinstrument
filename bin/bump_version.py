#!/usr/bin/env python3


from __future__ import annotations

import glob
import os
import subprocess
import sys
import urllib.parse
from pathlib import Path

import click
from packaging.version import InvalidVersion, Version

import pyinstrument

config = [
    # file path, version find/replace format
    ("setup.py", 'version="{}"'),
    ("pyinstrument/__init__.py", '__version__ = "{}"'),
    ("docs/conf.py", 'release = "{}"'),
]

RED = "\u001b[31m"
GREEN = "\u001b[32m"
OFF = "\u001b[0m"


@click.command()
def bump_version() -> None:
    current_version = pyinstrument.__version__

    try:
        commit_date_str = subprocess.run(
            [
                "git",
                "show",
                "--no-patch",
                "--pretty=format:%ci",
                f"v{current_version}^{{commit}}",
            ],
            check=True,
            capture_output=True,
            encoding="utf8",
        ).stdout
        cd_date, cd_time, cd_tz = commit_date_str.split(" ")

        url_opts = urllib.parse.urlencode({"q": f"is:pr merged:>{cd_date}T{cd_time}{cd_tz}"})
        url = f"https://github.com/joerick/pyinstrument/pulls?{url_opts}"

        print(f"PRs merged since last release:\n  {url}")
        print()
    except subprocess.CalledProcessError as e:
        print(e)
        print("Failed to get previous version tag information.")

    git_changes_result = subprocess.run(["git diff-index --quiet HEAD --"], shell=True)
    repo_has_uncommitted_changes = git_changes_result.returncode != 0

    if repo_has_uncommitted_changes:
        print("error: Uncommitted changes detected.")
        sys.exit(1)

    # fmt: off
    print(              'Current version:', current_version)  # noqa
    new_version = input('    New version: ').strip()
    # fmt: on

    try:
        Version(new_version)
    except InvalidVersion:
        print("error: This version doesn't conform to PEP440")
        print("       https://www.python.org/dev/peps/pep-0440/")
        sys.exit(1)

    actions = []

    for path_pattern, version_pattern in config:
        paths = [Path(p) for p in glob.glob(path_pattern)]

        if not paths:
            print(f"error: Pattern {path_pattern} didn't match any files")
            sys.exit(1)

        find_pattern = version_pattern.format(current_version)
        replace_pattern = version_pattern.format(new_version)
        found_at_least_one_file_needing_update = False

        for path in paths:
            contents = path.read_text(encoding="utf8")
            if find_pattern in contents:
                found_at_least_one_file_needing_update = True
                actions.append(
                    (
                        path,
                        find_pattern,
                        replace_pattern,
                    )
                )

        if not found_at_least_one_file_needing_update:
            print(f'''error: Didn't find any occurrences of "{find_pattern}" in "{path_pattern}"''')
            sys.exit(1)

    print()
    print("Here's the plan:")
    print()

    for action in actions:
        path, find, replace = action
        print(f"{path}  {RED}{find}{OFF} → {GREEN}{replace}{OFF}")

    print(f"Then commit, and tag as v{new_version}")

    answer = input("Proceed? [y/N] ").strip()

    if answer != "y":
        print("Aborted")
        sys.exit(1)

    for path, find, replace in actions:
        contents = path.read_text(encoding="utf8")
        contents = contents.replace(find, replace)
        path.write_text(contents, encoding="utf8")

    print("Files updated. If you want to update the changelog as part of this")
    print("commit, do that now.")
    print()

    while input('Type "done" to continue: ').strip().lower() != "done":
        pass

    subprocess.run(
        [
            "git",
            "commit",
            "--all",
            f"--message=Bump version: v{new_version}",
        ],
        check=True,
    )

    subprocess.run(
        [
            "git",
            "tag",
            "--annotate",
            f"--message=v{new_version}",
            f"v{new_version}",
        ],
        check=True,
    )

    print("Done.")


if __name__ == "__main__":
    os.chdir(Path(__file__).parent.parent.resolve())
    bump_version()
