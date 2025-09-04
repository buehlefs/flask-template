from pathlib import Path
from platform import system
from shutil import rmtree
from typing import List, Optional

from dotenv import load_dotenv
from invoke import task
from invoke.runners import Result
from invoke.context import Context

if system() == "Windows":
    from subprocess import list2cmdline as join
else:
    from shlex import join

load_dotenv(".flaskenv")
load_dotenv(".env")


# FIXME change this name after renaming the flask template package!
MODULE_NAME = "flask_template"


# a list of allowed licenses, dependencies with other licenses will trigger an error in the list-licenses command
ALLOWED_LICENSES = [
    "3-Clause BSD License",
    "Apache 2.0",
    "Apache License, Version 2.0",
    "Apache Software License",
    "BSD License",
    "BSD",
    "BSD-3-Clause",
    "GNU Lesser General Public License v2 or later (LGPLv2+)",
    "GNU Library or Lesser General Public License (LGPL)",
    "GPLv3",
    "MIT License",
    "MIT",
    "Mozilla Public License 2.0 (MPL 2.0)",
    "new BSD",
    "Python Software Foundation License",
]


@task
def doc(
    c: Context,
    format_: str = "html",
    all_: bool = False,
    color: bool = True,
    clean: bool = False,
):
    """Build the documentation.

    Args:
        c (Context): task context
        format_ (str, optional): the format to build. Defaults to "html".
        all (bool, optional): build all files new. Defaults to False.
        color (bool, optional): color output. Defaults to True.
        clean (bool, optional): try to clean up the build directory before building. Defaults to False.
    """
    if clean:
        for file_ in Path("./docs/_build").glob("*"):
            rmtree(file_, ignore_errors=True)
    cmd = ["sphinx-build", "-b", format_]
    if all_:
        cmd.append("-a")
    if color:
        cmd.append("--color")
    else:
        cmd.append("--no-color")
    cmd += [".", "_build"]
    with c.cd(str(Path("./docs"))):
        c.run(join(cmd), echo=True)


@task
def browse_doc(c: Context):
    """Open the documentation in the browser.

    Args:
        c (Context): task context
    """
    index_path = Path("./docs/_build/index.html")
    if not index_path.exists():
        doc(c)

    print(f"Open: file://{index_path.resolve()}")
    import webbrowser

    webbrowser.open_new_tab(str(index_path.resolve()))


@task
def doc_index(c: Context, filter_: str = ""):
    """Search the index of referencable sphinx targets in the documentation.

    Args:
        c (Context): task context
        filter_ (str, optional): an optional filter string. Defaults to "".
    """
    inv_path = Path("./docs/_build/objects.inv")
    if not inv_path.exists():
        doc(c)

    if filter_:
        filter_ = filter_.lower()

    with c.cd(str(Path("./docs"))):
        output: Optional[Result] = c.run(
            join(["python", "-m", "sphinx.ext.intersphinx", "_build/objects.inv"]),
            echo=True,
            hide="stdout",
        )
        stdout = output.stdout if output else ""
        print(
            "".join(
                l
                for l in stdout.splitlines(True)
                if (l and not l[0].isspace()) or (not filter_) or (filter_ in l.lower())
            ),
        )


@task
def list_licenses(
    c: Context,
    format_: str = "json",
    include_installed: bool = False,
    summary: bool = False,
    short: bool = False,
    echo: bool = False,
):
    """List licenses of dependencies.

    By default only the direct (and transitive) dependencies of the project are included.

    Args:
        c (Context): task context
        format_ (str, optional): The output format (json, html, markdown, plain, plain-vertical, rst, confluence, json-license-finder, csv). Defaults to "json".
        include_installed (bool, optional): If true all currently installed packages are considered dependencies. Defaults to False.
        summary (bool, optional): If true output a summary of found licenses. Defaults to False.
        short (bool, optional): If true only name, version, license and authors of a apackage are printed. Defaults to False.
        echo (bool, optional): If true the command used to generate the license output is printed to console. Defaults to False.
    """
    packages: List[str] = []
    if not include_installed:
        packages_output: Optional[Result] = c.run(
            join(["poetry", "export", "--dev", "--without-hashes"]),
            echo=False,
            hide="both",
        )
        packages_stdout = packages_output.stdout if packages_output else ""
        packages = [p.split("=", 1)[0] for p in packages_stdout.splitlines() if p]
    cmd: List[str] = [
        "pip-licenses",
        "--format",
        format_,
        "--with-authors",
        "--allow-only",
        ";".join(ALLOWED_LICENSES),
    ]
    if not short:
        cmd += [
            "--with-urls",
            "--with-description",
            "--with-license-file",
            "--no-license-path",
            "--with-notice-file",
        ]
    if summary:
        cmd.append("--summary")
    if not include_installed:
        cmd += [
            "--packages",
            *packages,
        ]
    c.run(
        join(cmd),
        echo=echo,
        warn=True,
    )


@task
def update_licenses(c: Context, include_installed: bool = False):
    """Update the licenses template to include all licenses.

    By default only the direct (and transitive) dependencies of the project are included.

    Args:
        c (Context): task context
        include_installed (bool, optional): Include all currently installed libraries. Defaults to False.
    """
    packages: List[str] = []
    if not include_installed:
        packages_output: Optional[Result] = c.run(
            join(["poetry", "export", "--dev", "--without-hashes"]),
            echo=False,
            hide="both",
        )
        packages_stdout = packages_output.stdout if packages_output else ""
        packages = [p.split("=", 1)[0] for p in packages_stdout.splitlines() if p]
    cmd: List[str] = [
        "pip-licenses",
        "--format",
        "html",
        "--output-file",
        str((Path(".") / Path(MODULE_NAME) / Path("templates/licenses.html")).resolve()),
        "--with-authors",
        "--with-urls",
        "--with-description",
        "--with-license-file",
        "--no-license-path",
        "--with-notice-file",
        "--allow-only",
        ";".join(ALLOWED_LICENSES),
    ]
    if not include_installed:
        cmd += [
            "--packages",
            *packages,
        ]
    result = c.run(
        join(cmd),
        echo=True,
        hide="err",
        warn=True,
    )
    if "not in allow-only licenses was found" in result.stderr:
        raise ValueError(
            "Encountered an unknown licence. Please check the licences of new or updated packages or update the ALLOWED_LICENCES.\n"
            + "\n--- COMMAND OUTPUT ---\n"
            + result.stderr
        )


@task(update_licenses)
def update_dependencies(c: Context):
    """Update dependencies that are derived from the pyproject.toml dependencies (e.g. doc dependencies and licenses).

    Args:
        c (Context): task context
    """
    c.run(
        join(
            [
                "poetry",
                "export",
                "--dev",
                "--format",
                "requirements.txt",
                "--output",
                str(Path("./docs/requirements.txt")),
            ]
        ),
        echo=True,
        hide="err",
        warn=True,
    )


@task()
def rename_project(c: Context, name: str):
    """Rename the project template to a different project name.

    WARNING: This will edit file cntents in the current project folder.
    WARNING: The rename will be done naively by matching the old name!

    This function can be removed once the project has been renamed.

    Args:
        c (Context): task context
        name (str): the new project name in snake case
    """
    git_status: Optional[Result] = c.run(
        join(["git", "status", "--porcelain"]), hide=True
    )
    if (
        git_status
        and git_status.ok
        and git_status.stdout
        and not git_status.stdout.isspace()
    ):
        # is in a git repo and not all changes are committed
        print("NOT IN A CLEAR GIT REPOSITORY! Aborting...")
        print("Please commit all changes before running this command!")
        return

    print("Current project name is:", repr(MODULE_NAME))
    print("NEW project name will be:", repr(name), "\n\n")

    old_name_parts = MODULE_NAME.split("_")
    new_name_parts = name.split("_")

    replacers = [
        ("_".join(old_name_parts), "_".join(new_name_parts)),
        ("-".join(old_name_parts), "-".join(new_name_parts)),
        (" ".join(old_name_parts), " ".join(new_name_parts)),
        (
            "_".join(map(lambda s: s.capitalize(), old_name_parts)),
            "_".join(map(lambda s: s.capitalize(), new_name_parts)),
        ),
        (
            "-".join(map(lambda s: s.capitalize(), old_name_parts)),
            "-".join(map(lambda s: s.capitalize(), new_name_parts)),
        ),
        (
            " ".join(map(lambda s: s.capitalize(), old_name_parts)),
            " ".join(map(lambda s: s.capitalize(), new_name_parts)),
        ),
        (
            "_".join(map(lambda s: s.title(), old_name_parts)),
            "_".join(map(lambda s: s.title(), new_name_parts)),
        ),
        (
            "-".join(map(lambda s: s.title(), old_name_parts)),
            "-".join(map(lambda s: s.title(), new_name_parts)),
        ),
        (
            " ".join(map(lambda s: s.title(), old_name_parts)),
            " ".join(map(lambda s: s.title(), new_name_parts)),
        ),
        (
            "".join(map(lambda s: s.title(), old_name_parts)),
            " ".join(map(lambda s: s.title(), new_name_parts)),
        ),
    ]

    # replace parts replaced in links to original github repo with original text
    re_replacer = ("buehlefs/" + "-".join(new_name_parts), "buehlefs/flask-template")

    root = Path(".").resolve()

    to_rename: List[Path] = []

    def replace_name(path: Path):
        if path.name in ("__pyache__", "_build"):
            return  # ignore cache files and docs build output

        # Rename project in file contents
        if path.is_file() and (
            path.suffix
            in (
                ".toml",
                ".md",
                ".rst",
                ".txt",
                ".py",
            )
            or path.name in (".flaskenv", ".gitignore")
        ):
            old = path.read_text()
            content = old
            for pattern, replacement in replacers:
                content = content.replace(pattern, replacement)
            # keep all links to original github repo intact
            content = content.replace(*re_replacer)
            if content != old:
                print("Updated:", "\n  ", path)
                path.write_text(content)
            else:
                print("Unchanged:", "\n  ", path)
        filename = path.name

        # mark for renaming
        for pattern, _ in replacers:
            if pattern in filename:
                to_rename.append(path)
                break

        # recurse into directories
        if path.is_dir():
            if path.name.startswith("."):
                return  # ignore hidden dirs
            for p in path.iterdir():
                replace_name(p)

    for p in root.iterdir():
        if p.name not in ("migrations", "instance", "typings", "translations"):
            replace_name(p)

    while to_rename:
        path = to_rename.pop()
        filename = path.name
        for pattern, replacement in replacers:
            if pattern in filename:
                new_path = path.parent / filename.replace(pattern, replacement)
                print("Renamed:", "\n  ", path, "\n  ", new_path)
                path.rename(new_path)
