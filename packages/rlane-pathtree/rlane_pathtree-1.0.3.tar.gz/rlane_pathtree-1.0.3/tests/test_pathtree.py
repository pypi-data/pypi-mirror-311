import io
import sys
from pathlib import Path

import pytest

from pathtree.cli import PathtreeCLI, main
from pathtree.pathtree import PathTree


def run_cli(options: list[str]) -> None:
    """Test calling the cli directly."""

    sys.argv = ["pathtree"]
    if options:
        sys.argv += options
    print(f"\nRunning {sys.argv!r}", flush=True)
    main()


def test_file_dev_null() -> None:
    run_cli(["/dev/null"])


def test_stdin(monkeypatch) -> None:
    print()

    lines = PathtreeCLI.dedent(
        """
    /root/top/bob
    /root/top/bob/george
    /root/top/bob/sally
    /root/top/bob/sally/ben
    /root/top/bob/sally/ben/ralph
        """
    )

    with io.StringIO(lines) as stdin:
        monkeypatch.setattr("sys.stdin", stdin)
        run_cli(["-"])


def test_prefix() -> None:
    print()
    PathtreeCLI.prefix = "woohoo"
    with pytest.raises(SystemExit) as err:
        main(["--help"])
    assert err.value.code == 0
    PathtreeCLI.prefix = None


def find_and_print(tree, name, expected=True):

    node = tree.find(name)
    if node:
        if expected:
            print(node)
        else:
            raise FileExistsError(name)
    elif expected:
        raise FileNotFoundError(name)


def test_one() -> None:
    print()
    paths = [
        Path("/root"),
        Path("/root/a-f"),
        Path("/root/b-d"),
        Path("/root/b-d/g-f"),
        Path("/root/b-d/h-d"),
        Path("/root/b-d/h-d/m-f"),
        Path("/root/c-f"),
        Path("/root/d-d"),
        Path("/root/d-d/i-f"),
        Path("/root/d-d/j-d"),
        Path("/root/d-d/j-d/domain"),
        Path("/root/d-d/j-d/domain/kingdom"),
        Path("/root/d-d/j-d/domain/kingdom/phylum"),
        Path("/root/d-d/j-d/n-f"),
        Path("/root/d-d/j-d/red"),
        Path("/root/d-d/j-d/red/yellow"),
        Path("/root/d-d/j-d/red/yellow/blue"),
        Path("/root/e-f"),
        Path("/root/f-d"),
        Path("/root/f-d/k-f"),
        Path("/root/f-d/l-d"),
        Path("/root/f-d/l-d/m-f"),  # collision in basename
        Path("/root/f-d/l-d/o-f"),
    ]

    tree = PathTree()
    for path in paths:
        tree.addpath(path)

    tree.print()
    find_and_print(tree, "/root/d-d")
    find_and_print(tree, "/root/d-d/j-d")


def test_two() -> None:
    print()
    tree = PathTree()
    tree.addpath(Path("bob"))
    tree.addpath(Path("bob/george"))
    tree.addpath(Path("bob/sally"))
    tree.addpath(Path("bob/sally/ben"))
    tree.addpath(Path("bob/sally/ben/ralph"))

    tree.print()
    find_and_print(tree, "bob")


def test_three() -> None:
    print()
    tree = PathTree()
    tree.addpath(Path("top/bob"))
    tree.addpath(Path("top/bob/george"))
    tree.addpath(Path("top/bob/sally"))
    tree.addpath(Path("top/bob/sally/ben"))
    tree.addpath(Path("top/bob/sally/ben/ralph"))

    tree.print()
    find_and_print(tree, "top")
    find_and_print(tree, "top/bob")


@pytest.mark.skip(reason="collapse not implemented")
def test_four() -> None:
    print()
    tree = PathTree()  # (collapse=True)
    tree.addpath(Path("top/bob"))
    tree.addpath(Path("top/bob/george"))
    tree.addpath(Path("top/bob/sally"))
    tree.addpath(Path("top/bob/sally/ben"))
    tree.addpath(Path("top/bob/sally/ben/ralph"))

    tree.print()
    find_and_print(tree, "top", expected=False)
    find_and_print(tree, "top/bob")


@pytest.mark.skip(reason="collapse not implemented")
def test_four_2() -> None:
    print()
    tree = PathTree()  # (collapse=True)
    tree.addpath(Path("/top/bob"))
    tree.addpath(Path("/top/bob/george"))
    tree.addpath(Path("/top/bob/sally"))
    tree.addpath(Path("/top/bob/sally/ben"))
    tree.addpath(Path("/top/bob/sally/ben/ralph"))

    tree.print()
    find_and_print(tree, Path("/top"), expected=False)
    find_and_print(tree, Path("/top/bob"))


@pytest.mark.skip(reason="collapse not implemented")
def test_five() -> None:
    print()
    tree = PathTree()  # (collapse=True)
    tree.addpath(Path("root/top/bob"))
    tree.addpath(Path("root/top/bob/george"))
    tree.addpath(Path("root/top/bob/sally"))
    tree.addpath(Path("root/top/bob/sally/ben"))
    tree.addpath(Path("root/top/bob/sally/ben/ralph"))

    tree.print()
    find_and_print(tree, Path("root"), expected=False)
    find_and_print(tree, Path("root/top"), expected=False)
    find_and_print(tree, Path("root/top/bob"))


@pytest.mark.skip(reason="collapse not implemented")
def test_five_2() -> None:
    print()
    tree = PathTree()  # (collapse=True)
    tree.addpath(Path("/root/top/bob"))
    tree.addpath(Path("/root/top/bob/george"))
    tree.addpath(Path("/root/top/bob/sally"))
    tree.addpath(Path("/root/top/bob/sally/ben"))
    tree.addpath(Path("/root/top/bob/sally/ben/ralph"))

    tree.print()
    find_and_print(tree, Path("/root"), expected=False)
    find_and_print(tree, Path("/root/top"), expected=False)
    find_and_print(tree, Path("/root/top/bob"))
